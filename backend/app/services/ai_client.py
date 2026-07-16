"""Model adapter: one narrow place to configure or replace the LLM provider."""

from flask import current_app


class ModelServiceError(Exception):
    """A configured model provider could not complete a request."""


def generate_grounded_response(task, question, source_blocks):
    """Ask the configured model to use only retrieved study passages.

    A deterministic fallback keeps local setup useful when no API key has been
    configured. Production should set OPENAI_API_KEY so this function invokes
    the model service.
    """
    context = "\n\n".join(
        f"[Source {number}: {title}]\n{excerpt}"
        for number, title, excerpt in source_blocks
    )
    prompt = f"""You are StudyMate AI, a careful study assistant.
Task: {task}
Question or instruction: {question}

Use only the numbered source passages below. Do not add outside facts. If the
passages do not support an answer, say that clearly. Cite claims inline with
[Source N]. Keep the response concise and helpful for a student.

Retrieved passages:
{context}
"""
    api_key = current_app.config["OPENAI_API_KEY"]
    if not api_key:
        return None

    # Imported only when configured so local development does not require a key.
    from openai import OpenAI

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=current_app.config["OPENAI_MODEL"],
            input=prompt,
        )
        return response.output_text.strip()
    except Exception as exc:
        current_app.logger.exception("Configured model request failed")
        raise ModelServiceError("The study model is temporarily unavailable. Please try again shortly.") from exc
