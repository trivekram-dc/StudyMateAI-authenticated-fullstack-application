# StudyMate AI

StudyMate AI is an authenticated, full-stack study assistant that keeps a student's notes organized by course and turns those notes into source-backed answers, summaries, and practice questions.

## MVP capabilities

- JWT registration, sign-in, session restoration, and protected frontend routes.
- Private course and study-material CRUD, enforced by backend ownership checks.
- A relational SQLite data model: `User` → `Course` → `StudyMaterial`.
- Text-first study materials (notes, readings, and slides) to keep the MVP dependable.
- A local retrieval workflow that chunks content, ranks matching passages, and returns them as visible sources.
- Summary, ask, and quiz endpoints connected to the study assistant UI.

## Project layout

```text
backend/       Flask REST API, SQLAlchemy models, JWT auth, retrieval service
frontend/      React + Vite client and protected study workspace
```

## Run locally

### API

1. Create and activate a virtual environment in `backend`.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and replace the development secrets.
4. Start the API: `python run.py`

The API starts at `http://localhost:5000`; its health endpoint is `GET /api/health`.

### Client

1. In `frontend`, copy `.env.example` to `.env` if the API is not running at its default address.
2. Install packages: `npm install`
3. Start the client: `npm run dev`

Open the local address shown by Vite (normally `http://localhost:5173`).

## Key endpoints

| Area | Endpoints |
| --- | --- |
| Auth | `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me` |
| Courses | `GET, POST /api/courses`, `GET, PUT, DELETE /api/courses/:id` |
| Materials | `GET, POST /api/materials`, `GET, PUT, DELETE /api/materials/:id` |
| Study tools | `POST /api/ai/summarize`, `POST /api/ai/ask`, `POST /api/ai/quiz` |

All endpoints other than registration, login, and health require an `Authorization: Bearer <JWT>` header.

## Retrieval note

The MVP uses a lightweight local, keyword-ranked retrieval layer so it works without an external key or vector database. It preserves the RAG product flow—ingestion, chunking, retrieval, response, and cited passages—and gives a safe foundation for a later OpenAI embeddings/vector-store upgrade.

## Test the API

From `backend`, run:

```text
python -m unittest discover -s tests
```

The tests cover user-boundary enforcement and source-backed retrieval.

---

## Original capstone pitch

Deliverable 1: Business Problem Scenario
For my capstone project, I want to build an AI study assistant for students. The main idea is to create a web app where students can upload or save their course materials, organize them by class or topic, and then use AI to get summaries, ask questions, and generate quiz questions based on their own study content.

Target User
The main users for this app are students, especially college students or independent learners who have a lot of notes, readings, and study materials to manage.

Domain or Industry
This project fits into the education / EdTech space.

Business or User Problem
A lot of students deal with large amounts of information across different courses, and it can get overwhelming to stay organized and study effectively. Students often have notes in different places, and when it’s time to review, they have to spend a lot of time searching through materials or making summaries themselves.

There are already AI tools that can summarize or answer questions, but most of them are very general. They usually don’t focus on a student’s own materials, and they may give answers that sound good but are not actually based on the student’s notes. That makes it hard to trust the output.

This app is meant to solve that problem by giving students a way to work with their own content in a more organized and useful way.

Why the Problem Matters
This matters because students need better tools for studying, especially when classes move fast and there is a lot of reading or note-taking involved. If students can upload their own materials and get answers or summaries based on those materials, it can save time and make studying more effective.

It also matters from a trust perspective. If the AI gives source-backed responses instead of random answers, students can feel more confident using it.

What Users Currently Struggle With
Right now, students often struggle with:

keeping their notes and materials organized,
reviewing long readings or lecture notes quickly,
making summaries manually,
testing themselves on material,
and knowing whether an AI-generated answer is actually reliable.
What Success Should Look Like
A successful version of this app would let a student:

sign up and log in securely,
create and manage their own courses or topics,
upload or save study materials,
ask questions about those materials,
get summaries and quiz questions,
and see what sources the AI used when generating its answer.
The biggest sign of success is that the app feels useful for real studying, not just like a generic chatbot.

Deliverable 2: Problem-Solving Process
MVP Feature List
For the MVP, I want to focus on the core features that make the app functional and meet the capstone requirements.

Authentication / Authorization
User sign up
User login/logout
Protected routes
Users can only access their own courses and study materials
Main App Features
Create courses or study categories
Upload or save study materials
View and manage uploaded materials
Organize materials under a course
AI / RAG Features
Generate a summary from study material
Ask questions about uploaded material
Generate quiz questions from selected content
Show the source content used in the AI response
Full-Stack Features
React frontend
Flask backend API
SQL database with related models
CRUD operations for core resources
Stretch Features
If I have extra time after the MVP is working, I would like to add:

flashcard generation
quiz scoring or saved quiz history
search/filtering for materials
PDF upload improvements
better source highlighting
study history or analytics
a cleaner dashboard with more polished UI features
Planned Authentication Approach
For authentication, I plan to use JWT-based auth in Flask. Users will be able to register and log in, and once logged in, they will receive a token that the frontend will use when making protected API requests.

Passwords will be hashed before being stored, and backend routes will check the logged-in user before allowing access to any protected resources. This is important because every user’s study materials should stay private.

Planned SQL Data Model and Relationships
I plan to use a SQL database like PostgreSQL or SQLite during development.

Here are the main models I’m planning:

User
id
username
email
password_hash
created_at
Course
id
user_id
title
description
created_at
StudyMaterial
id
user_id
course_id
title
content or file path
material_type
created_at
AIInteraction (possibly MVP, or maybe after core features are working)
id
user_id
study_material_id or course_id
prompt
response
interaction_type
created_at
Relationships
One user can have many courses
One user can have many study materials
One course belongs to one user
One course can have many study materials
One study material belongs to one course
One user can have many AI interactions
This structure should satisfy the relational data requirement and also make it easier to organize content by user and by course.

Planned Frontend Views or Pages
Right now, I expect the app to have these main pages:

Landing page
Register page
Login page
Dashboard
Courses page
Course detail page
Upload / create material page
Study assistant page for summaries, Q&A, and quizzes
If I have time, I may also add a profile/settings page.

Planned Backend API Routes
Some of the main API routes I plan to build are:

Auth
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
Courses
GET /api/courses
POST /api/courses
GET /api/courses/<id>
PUT /api/courses/<id>
DELETE /api/courses/<id>
Study Materials
GET /api/materials
POST /api/materials
GET /api/materials/<id>
PUT /api/materials/<id>
DELETE /api/materials/<id>
AI
POST /api/ai/summarize
POST /api/ai/ask
POST /api/ai/quiz
Planned AI/RAG Workflow
The AI part of the app is supposed to do more than just generate text. I want it to actually use the student’s uploaded materials as the basis for responses.

My plan is:

The user uploads or saves study content.
The backend processes that content.
The content is split into chunks.
Those chunks are turned into embeddings.
The embeddings are stored in a retrieval system or vector store.
When the user asks a question, the app retrieves the most relevant chunks.
Those chunks are included in the prompt sent to the language model.
The model generates a response based on that context.
The app shows both the answer and the source content used.
I also want summaries and quizzes to be based on the same content, so the AI feature stays connected to the main purpose of the app.

Deliverable 3: Timeline and Scope
Phase 1: Plan and Pitch
In Phase 1, I will focus on planning the project before writing too much code.

This includes:

defining the problem clearly,
narrowing down the MVP,
designing the database models,
planning frontend pages,
listing backend routes,
planning the AI/RAG workflow,
deciding how the knowledge base will work,
and thinking through deployment and technical risks.
For the knowledge base, I plan to use user-uploaded study materials. I may start with text input first and then support PDF upload if time allows.

Some open questions I still need to figure out:

whether to support PDF upload in the MVP or save it for later,
whether to store AI interactions in the database,
and what vector store option is the most realistic for this project.
Phase 2: Build MVP
In Phase 2, I will build the main version of the app.

This phase includes:

setting up the Flask backend,
setting up the React frontend,
building authentication,
creating the database models and relationships,
building CRUD routes for courses and materials,
connecting frontend and backend,
implementing the AI/RAG workflow,
and showing the source-backed results.
I also want to have enough working by the end of this phase so I can share it for critique and get feedback.

Phase 3: Finish and Showcase
In Phase 3, I will improve the app and get it ready for final submission.

This phase includes:

improving the UI and user experience,
reviewing authorization carefully,
improving AI response quality,
writing documentation,
deploying the frontend and backend,
testing the deployed app,
recording a demo,
and writing a final reflection.
If I still have time, this is when I would add stretch features like flashcards or better search tools.

Technical Risks or Blockers
A few risks I already see are:

1. File upload and parsing could be more complicated than expected
If I support PDFs or different file types, text extraction might be messy or unreliable.

Plan: Start with plain text or simple content input first, then add more advanced file support later if possible.

2. The RAG workflow may take longer than expected
Chunking, embeddings, retrieval, and source display are all connected, so debugging could take time.

Plan: Keep the first AI use case simple, probably question answering from uploaded text, and expand from there.

3. Authorization mistakes could expose user data
Since users will have private study materials, it is important to make sure one user cannot access another user’s data.

Plan: Build ownership checks into routes early and test them often.

Tools or Concepts I May Need to Review
Some topics I may need to spend more time reviewing are:

Flask JWT authentication
SQLAlchemy relationships
React protected routes
file upload handling in Flask
embeddings and vector stores
prompt design for grounded AI responses
deployment setup and environment variables
Where I Expect to Revise After Critique
After getting feedback, I expect I may need to revise:

the MVP scope,
the user interface,
the AI response flow,
how I show sources,
or parts of the data model if something feels too complex or unnecessary.
What I Will Cut If the Project Gets Too Large
If the project starts becoming too big, I will cut features in this order:

flashcards
advanced quiz features
PDF support
saved AI interaction history
analytics or dashboard extras
The parts I will not cut are:

authentication,
protected user data,
relational models,
CRUD features,
and one working AI/RAG feature with sources.
Deliverable 4: Technical Feasibility and Risk Plan
Why This Project Is Feasible
I think this project is realistic for the capstone timeline because I can scope it carefully and focus on a simple but meaningful MVP. The app has a clear purpose, and each major part supports the capstone requirements: authentication, SQL relationships, protected resources, and a source-backed AI feature.

What Must Work for the MVP
For the MVP to count as successful, these things need to work:

users can register and log in,
users can create and manage their own courses and materials,
users cannot access each other’s data,
users can ask a question or request a summary,
the app retrieves relevant content,
and the response includes source-backed support.
What Is Intentionally Out of Scope
For now, I am intentionally leaving out:

advanced analytics,
collaboration between users,
instructor/admin tools,
detailed progress tracking,
and more advanced AI study tools unless the core version is already complete.
Most Technically Risky Parts
The most technically risky parts are:

file ingestion and parsing,
setting up embeddings and retrieval,
making sure source-backed results are actually useful,
and deploying a full-stack AI app with multiple moving parts.
How I Will Reduce Risk Early
To reduce risk early, I plan to:

start with a smaller MVP,
use plain text before complex file upload,
build auth and ownership first,
get CRUD routes working before polishing UI,
and implement one AI workflow before adding more features.
How I Will Keep the AI Feature Connected to the Main App
I want the AI feature to feel like part of the product, not something random added at the end. To do that, the AI will only work on the user’s uploaded study materials, and responses will be tied to those materials. That way, the AI is directly supporting the student’s actual workflow.

How I Will Check Whether the AI Feature Is Useful
I will test whether the AI feature is useful by checking:

if it answers questions clearly,
if the answer matches the source material,
if the sources shown are relevant,
and if the output would actually help someone studying.
Deployment Plan
My likely deployment plan is:

Frontend: Vercel or Netlify
Backend: Render or Railway
Database: PostgreSQL
LLM/API: OpenAI API or similar
Retrieval/vector system: a simple option that is manageable for this capstone, possibly Chroma or another lightweight setup
Production Environment Variables
I will use environment variables for things like:

database URL,
secret key,
JWT secret,
API keys,
and frontend/backend URLs.
These will be stored in the deployment platform settings instead of hardcoded into the app.

How the Deployed App Will Work End-to-End
In production:

the frontend will send requests to the deployed Flask backend,
the backend will connect to the production database,
the backend will access the retrieval system or vector store,
and the backend will call the model API securely using environment variables.
To verify that deployment works, I will test the full user flow:

create an account
log in
create a course
upload or save material
ask a question
get a source-backed response
confirm another user cannot access that content
test logout and route protection
If all of that works, then the deployed app should meet the main capstone goals.

Conclusion
Overall, I think this project is a good fit for the capstone because it combines all of the main course skills into one application: React, Flask, authentication, databases, protected user data, and AI/RAG. It also solves a real problem in a way that feels practical and portfolio-worthy.

My goal is to keep the MVP focused, make sure the core user flow works well, and build an AI feature that is actually useful and grounded in the user’s own study materials.
