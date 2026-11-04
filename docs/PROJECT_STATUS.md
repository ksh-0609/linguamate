# LinguaMate: Project Status

_Last updated: 2026-11-04_

**Current position:** Phase 1 is complete. Next up: Phase 2 (database foundation).

## Phase tracker

| Phase | Name | Status |
|---|---|---|
| 1 | Environment, repository, skeleton, config, `/health` | Done |
| 2 | PostgreSQL in Docker, SQLAlchemy models, Alembic | Not started |
| 3 | LLM layer, structured output, first grammar endpoint | Not started |
| 4 | Authentication, profiles, onboarding | Not started |
| 5 | Core services: mistakes, vocabulary and spaced repetition, quizzes | Not started |
| 6 | LangGraph MVP: router, conversation and grammar nodes, tools, memory | Not started |
| 7 | RAG with Qdrant: ingestion, retrieval, hybrid search, reranking | Not started |
| 8 | Planner and analysis nodes, dashboard, analytics | Not started |
| 9 | Reading and writing modules | Not started |
| 10 | Voice: speech-to-text, text-to-speech, pronunciation | Not started |
| 11 | Evaluation suite and measured results | Not started |
| 12 | Security and reliability hardening | Not started |
| 13 | Docker Compose and cloud deployment | Not started |
| 14 | Documentation, demo, experiment, interview prep | Not started |

Milestones: **M1** end of Phase 5 (working non-agentic tutor), **M2** end of Phase 7
(agentic + RAG), **M3** end of Phase 9 (full learning loop), **M4** Phase 14 (complete).

## Phase 1 report

### Completed features
- Python 3.13 virtual environment, project installed in editable mode
- Git repository with a `.gitignore` that protects secrets and local data
- Typed, validated settings loaded from environment variables and `.env`
- Central logging configuration
- FastAPI application factory with a `GET /health` endpoint and Swagger docs at `/docs`
- Pydantic response schema for the health endpoint
- Automated tests with pytest

### Files created
- Root: `.gitignore`, `.env.example`, `pyproject.toml`, `requirements.lock.txt`,
  `README.md`, `PROJECT_STATUS.md`
- `src/linguamate/__init__.py`
- `src/linguamate/core/` : `config.py`, `logging_config.py`
- `src/linguamate/schemas/` : `health.py`
- `src/linguamate/api/` : `main.py`, `routers/health.py`
- `tests/` : `test_health.py`, `test_config.py`
- `docs/` : `ARCHITECTURE.md`, `ER_DIAGRAM.md`, `ROADMAP.md`

### Tests
- Passed: 4. Failed: 0.
- Run locally on Windows with Python 3.13.5 using `pytest`.

### Known issues and watch-list
- Docker has not been checked yet (needed at the start of Phase 2).
- Compatibility of the local speech engine with Python 3.13 on Windows is unverified.
  Test it before Phase 10. Fallback: a second environment with an older Python for that module.
- The version number is defined twice (`pyproject.toml` and `src/linguamate/__init__.py`).
  Keep them equal.
- Settings read `.env` from the current working directory, so always run commands
  from the project root.
- `pyproject.toml` declares minimum versions. Exact tested versions are in `requirements.lock.txt`.
- No continuous integration yet.

### Pending tasks
- Phase 2 onward as listed in the tracker.

### Next phase
Phase 2: database foundation (Docker check, PostgreSQL container, SQLAlchemy models, Alembic).

## Decision log

| Decision | Reason |
|---|---|
| Python 3.13.5 | Already installed; no confirmed benefit from a second Python |
| `src/` layout with editable install | Prevents accidental imports from the wrong folder |
| `httpx2` added to dev dependencies | Starlette's TestClient now prefers it and warns when only `httpx` is present |
| One LangGraph graph; "agents" are specialised nodes | Avoids multi-agent complexity for its own sake |
| Deterministic services first, agents later | Agent tools wrap tested services, keeping the agent layer thin |
| Repository private until the final phase | Public release only after reviewing for secrets |

## Conventions (keep consistent)

- Environment variables are UPPER_SNAKE_CASE and match the field names in `Settings`.
- Python modules and functions use snake_case; classes use PascalCase.
- Pydantic schemas live in `schemas/`; one router per feature in `api/routers/`.
- Business logic lives in `services/`. Endpoints never call an LLM directly.
- Real secrets live only in `.env`, which is never committed.