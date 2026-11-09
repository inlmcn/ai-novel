# AI Novel Studio

AI-assisted novel writing and independent editorial quality-control platform.

## Product scope

- Novel projects, outlines, characters, worldbuilding, and chapter management
- Immutable chapter versions and traceable revisions
- Independent Writer, Reviewer, Judge, and Editor agents
- Long-form story memory with structured facts and semantic retrieval
- Editorial reports, evidence-linked issues, and submission-readiness diagnostics

## Technology direction

- Frontend: Vue 3, TypeScript, Vite, Pinia
- Backend: Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2 async
- Workflow: LangGraph
- Persistence planned for later milestones: PostgreSQL + pgvector
- Queue/cache planned for later milestones: Redis

## M0: run without Docker

M0 deliberately has **no Docker, PostgreSQL, or Redis startup dependency**. The health endpoint and frontend shell can be developed independently.

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
PYTHONPATH=backend uvicorn app.main:app --reload --app-dir backend
```

Health endpoint: `http://127.0.0.1:8000/api/v1/health`.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://127.0.0.1:5173`.

### Environment

Copy `.env.example` to `.env` if you need to override settings. Database and Redis settings are placeholders for later milestones; M0 does not connect to either service.

## Engineering principles

1. Writer and Reviewer are separate roles; review evidence must be independently generated.
2. Chapter versions are append-only. Review reports are bound to an exact version.
3. Approval is an explicit Judge decision, not a simple majority vote.
4. Only approved manuscript content may update active story memory.
5. Every model run, review, revision, and decision must be traceable.
6. AI-generated quality scores are diagnostics, not guarantees of publication acceptance.

## Current status

M0 bootstrap is on `feat/bootstrap`. The API health endpoint and Vue shell are scaffolding. SQLAlchemy model definitions and the Alembic environment are early M1 groundwork, not yet a validated database migration. No local build, dependency installation, migration, or test execution has been performed in this environment.
