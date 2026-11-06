# AI Novel Studio

AI-assisted novel writing and independent editorial quality-control platform.

## Product scope

- Novel projects, outlines, characters, worldbuilding, and chapter management
- Immutable chapter versions and traceable revisions
- Independent Writer, Reviewer, Judge, and Editor agents
- Long-form story memory with structured facts and semantic retrieval
- Editorial reports, evidence-linked issues, and submission-readiness diagnostics

## Technology

- Frontend: Vue 3, TypeScript, Vite, Pinia
- Backend: Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2 async
- Workflow: LangGraph
- Data: PostgreSQL + pgvector; Redis for queueing and event delivery

## Local development

1. Copy `.env.example` to `.env` and adjust credentials if needed.
2. Start infrastructure: `docker compose up -d`.
3. Install backend dependencies: `python -m pip install -e '.[dev]'`.
4. Start API: `PYTHONPATH=backend uvicorn app.main:app --reload --app-dir backend`.
5. Install frontend dependencies: `cd frontend && npm install`.
6. Start frontend: `npm run dev`.

API health endpoint: `GET /api/v1/health`.

## Engineering principles

1. Writer and Reviewer are separate roles; review evidence must be independently generated.
2. Chapter versions are append-only. Review reports are bound to an exact version.
3. Approval is an explicit Judge decision, not a simple majority vote.
4. Only approved manuscript content may update active story memory.
5. Every model run, review, revision, and decision must be traceable.
6. AI-generated quality scores are diagnostics, not guarantees of publication acceptance.

## Current status

Bootstrap baseline is on `feat/bootstrap`. The API health endpoint and Vue shell are scaffolding only. Database models, migrations, authentication, LLM gateway, agent workflow, and production tests are not implemented yet.
