# AI Novel Studio

AI-assisted novel writing and independent editorial quality-control platform.

## Product scope

- Novel projects, outlines, characters, worldbuilding, and chapter management
- Immutable chapter versions and traceable revisions
- Independent Writer, Reviewer, Judge, and Editor agents
- Long-form story memory with structured facts and semantic retrieval
- Editorial reports, evidence-linked issues, and submission-readiness diagnostics

## Architecture direction

- Frontend: Vue 3, TypeScript, Vite, Pinia
- Backend: Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2 async
- Workflow: LangGraph
- Data: PostgreSQL + pgvector; Redis for queueing and event delivery
- Deployment: Docker Compose for local development; modular monolith API plus worker

## Engineering principles

1. Writer and Reviewer are separate roles; review evidence must be independently generated.
2. Chapter versions are append-only. Review reports are bound to an exact version.
3. Approval is an explicit Judge decision, not a simple majority vote.
4. Only approved manuscript content may update active story memory.
5. Every model run, review, revision, and decision must be traceable.
6. AI-generated quality scores are diagnostics, not guarantees of publication acceptance.

## Status

Repository bootstrap. Implementation status and setup instructions will be updated as milestones land.
