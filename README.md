# StudyMate AI

StudyMate AI is a source-backed study assistant for college students and independent learners. It gives each student a private workspace for course notes and readings, then helps them ask questions, make summaries, and create self-test quizzes from their own materials.

## The problem

Students often have notes and readings scattered across courses and must spend time finding information, making summaries, and checking whether an AI answer can be trusted. StudyMate keeps materials organized by course and displays the passages used to support every study response.

## MVP features

- Email/password registration, login, logout, and current-user session check.
- JWT-protected API routes and protected React pages.
- User-owned course and text-material management.
- Course creation, viewing, updating, and deletion; deleting a course removes its related materials.
- Study material creation, viewing, updating through the API, and deletion from the course view.
- Source-backed question answering, summary generation, and quiz generation.
- Clear loading, empty, and error states across the main user flow.

## Technology

| Layer | Tools |
| --- | --- |
| Frontend | React, React Router, Vite, CSS |
| Backend | Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-CORS |
| Database | SQLite locally; PostgreSQL-ready through `DATABASE_URL` |
| AI | OpenAI Responses API (when configured) |
| Retrieval | Local document chunking and keyword ranking for the MVP knowledge base |

## Data model

```text
User 1 ──< Course 1 ──< StudyMaterial
  └──────────────────< StudyMaterial
```

- **User:** account identity, email, hashed password, and ownership boundary.
- **Course:** a user-owned class or topic.
- **StudyMaterial:** a user-owned text source assigned to one course. It can be a note, reading, or slide content.

All protected resource queries include the current user ID. A resource owned by another user returns `404`, so users cannot list, read, modify, or delete each other's data.

## Authentication flow

Registration hashes the password using Werkzeug before saving the user. Login returns a signed JWT, which the React client stores as its session and sends in an `Authorization: Bearer <token>` header. On refresh, the client calls `GET /api/auth/me` to verify and restore the logged-in user. Logout removes the local session; every protected API endpoint independently validates the token and resource ownership.

## AI/RAG workflow

1. A student saves text study material under a course; this is the private knowledge base.
2. The API normalizes and splits material into overlapping chunks.
3. For a question, relevant chunks are ranked against the question across only that user's permitted materials.
4. If there are no relevant chunks, the API refuses to invent an answer and asks for a more specific question or more material.
5. The retrieved passages are inserted as numbered sources into a grounded prompt.
6. When `OPENAI_API_KEY` is configured, the backend sends that prompt to the OpenAI Responses API and returns the generated answer.
7. The frontend displays the answer and the supporting source excerpts.

For local setup without an API key, the app remains usable in **Local Study Mode**: it returns a deterministic response from the retrieved content and labels that mode in the interface. This is intentionally a development fallback, not the production AI configuration.

Example tasks:

- Add biology notes and ask, “What does the nucleus do?”
- Select a lecture and choose **Summarize**.
- Select a reading and choose **Make quiz**.

## Local setup

### Backend

From `backend`:

```bash
python3 -m venv .venv
source .venv/bin/activate              # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env                    # Windows PowerShell: Copy-Item .env.example .env
python run.py
```

The API is available at `http://localhost:5000`.

### Frontend

From `frontend` in a second terminal:

```bash
cp .env.example .env                    # Windows PowerShell: Copy-Item .env.example .env
npm install
npm run dev
```

Open the Vite address shown in the terminal, normally `http://localhost:5173`.

## Environment variables

Backend (`backend/.env`):

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Flask secret used outside JWT operations |
| `JWT_SECRET_KEY` | JWT signing secret; use a unique long random value in production |
| `DATABASE_URL` | SQLAlchemy connection URL; defaults to local SQLite |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins |
| `OPENAI_API_KEY` | Required for production model-generated responses |
| `OPENAI_MODEL` | Model used by the Responses API; defaults to `gpt-5-mini` |

Frontend (`frontend/.env`):

| Variable | Purpose |
| --- | --- |
| `VITE_API_URL` | Public backend base URL, ending in `/api` |

Never commit `.env` files or API keys. The repository contains only `.env.example` templates.

## Reviewer demo data

With the backend environment active, run:

```bash
python seed.py
```

This creates a local demo account:

```text
Email: demo@studymate.local
Password: DemoPass123!
```

It also creates a Biology course with sample cell-structure notes. Do not use this predictable account in a public deployment.

## API routes

| Method | Route | Description |
| --- | --- | --- |
| POST | `/api/auth/register` | Register a user and return a JWT |
| POST | `/api/auth/login` | Log in and return a JWT |
| POST | `/api/auth/logout` | Revoke the current JWT and end the session |
| GET | `/api/auth/me` | Return the authenticated user |
| GET/POST | `/api/courses` | List or create the current user's courses |
| GET/PUT/DELETE | `/api/courses/:id` | Read, update, or delete an owned course |
| GET/POST | `/api/materials` | List or create the current user's materials |
| GET/PUT/DELETE | `/api/materials/:id` | Read, update, or delete an owned material |
| POST | `/api/ai/ask` | Answer a question using retrieved material sources |
| POST | `/api/ai/summarize` | Summarize one owned material |
| POST | `/api/ai/quiz` | Create quiz questions from one owned material |

## Verification

Run backend tests from `backend`:

```bash
python -m unittest discover -s tests
```

The tests verify that another authenticated user cannot access a course or material they do not own, and that a relevant study question returns a source.

Manual verification checklist:

1. Register two accounts.
2. Create a course and material as the first account.
3. Verify the second account cannot see or request the first account's resources.
4. Ask a question based on the saved material and check the source card.
5. Log out and confirm protected pages redirect to login.

## Deployment notes

The intended production deployment is a Vite frontend on Vercel or Netlify and Flask API on Render or Railway, with PostgreSQL configured through `DATABASE_URL`.

Set the backend's `CORS_ORIGINS` to the deployed frontend URL, set `VITE_API_URL` to the deployed backend `/api` URL, use new production secrets for `SECRET_KEY` and `JWT_SECRET_KEY`, and configure `OPENAI_API_KEY` in the hosting provider's secret manager. After deployment, complete the manual verification checklist above using the public URL.

**Current limitation:** this repository does not yet include a deployed public URL. Deployment is the final operational step; the application is configured to deploy without code changes once the hosting accounts and production variables are supplied.

## Scope changes and future improvements

The approved MVP proposed embeddings and a vector store. To protect the core student workflow and make local review reliable, Version 1 uses local chunking and keyword retrieval, while retaining the full source-backed RAG sequence and a production model API adapter. Embeddings and a vector database are the next planned upgrade.

Other future improvements: PDF ingestion, material edit UI, persisted AI interaction history, flashcards, quiz scoring, search and filtering, richer source highlighting, and a polished deployed production environment.
