import re
from collections import Counter


WORD_RE = re.compile(r"[a-zA-Z0-9']+")


def chunks(text, size=700, overlap=120):
    normalized = " ".join(text.split())
    if not normalized:
        return []
    result, start = [], 0
    while start < len(normalized):
        end = min(len(normalized), start + size)
        if end < len(normalized):
            boundary = normalized.rfind(" ", start, end)
            end = boundary if boundary > start else end
        result.append(normalized[start:end])
        if end == len(normalized):
            break
        start = max(end - overlap, start + 1)
    return result


def retrieve(materials, query, limit=3):
    query_terms = Counter(WORD_RE.findall(query.lower()))
    ranked = []
    for material in materials:
        for index, chunk in enumerate(chunks(material.content)):
            terms = Counter(WORD_RE.findall(chunk.lower()))
            score = sum(query_terms[term] * terms[term] for term in query_terms)
            if score:
                ranked.append((score, material, index, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[:limit]


def sources_for(results):
    return [
        {"materialId": material.id, "materialTitle": material.title, "chunkIndex": index + 1, "excerpt": chunk, "relevance": score}
        for score, material, index, chunk in results
    ]


def summarize(material):
    text = " ".join(material.content.split())
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) <= 3:
        return text
    frequencies = Counter(WORD_RE.findall(text.lower()))
    scored = []
    for position, sentence in enumerate(sentences):
        words = WORD_RE.findall(sentence.lower())
        score = sum(frequencies[word] for word in words) / max(len(words), 1)
        scored.append((score, position, sentence))
    return " ".join(item[2] for item in sorted(sorted(scored, reverse=True)[:3], key=lambda item: item[1]))


def generate_quiz(material, count=3):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(material.content.split())) if len(s.split()) >= 6]
    questions = []
    for sentence in sentences[:count]:
        words = [word for word in WORD_RE.findall(sentence) if len(word) > 5]
        answer = max(words, key=len) if words else sentence.split()[0]
        question = sentence.replace(answer, "_____", 1)
        questions.append({"question": f"Fill in the blank: {question}", "answer": answer, "explanation": sentence})
    return questions
