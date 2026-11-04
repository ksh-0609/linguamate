# LinguaMate Roadmap

> Planned work. Actual progress is tracked in `PROJECT_STATUS.md`.
> Pytest tests are written in every phase. Phase 11 formalises the evaluation datasets.

| Phase | Goal | Done when |
|---|---|---|
| 1 | Environment, repo, skeleton, config, `/health` | Health endpoint responds, tests pass, code on GitHub |
| 2 | PostgreSQL in Docker, SQLAlchemy models, Alembic | Migrations apply and all tables exist |
| 3 | LLM layer: provider factory, structured output, token tracking, prompts, first grammar endpoint | Validated JSON correction returned |
| 4 | Authentication, profiles, onboarding API plus Streamlit login and onboarding | Register, log in and save a profile end to end |
| 5 | Core services: mistakes store, vocabulary with spaced repetition, quizzes with validated answer keys | Services unit-tested, basic Streamlit pages |
| 6 | LangGraph MVP: state, supervisor, conversation and grammar nodes, tools, checkpointer, traces | Tutor chat routes correctly and keeps context |
| 7 | RAG: ingestion, chunking, embeddings, Qdrant, filters, grounded answers with sources, then hybrid search and reranking | Retrieval metrics measured, answers cite sources |
| 8 | Planner and analysis nodes, dashboard, analytics charts | Dashboard shows real database numbers |
| 9 | Reading and writing modules | Level-based passages, essay feedback |
| 10 | Voice: speech-to-text, text-to-speech, pronunciation assessment | Record, transcribe, speak and score |
| 11 | Evaluation suite: 50 then 100+ cases, RAG and routing metrics, adversarial tests | Measured results reported as they come out |
| 12 | Security and reliability hardening | Rate limits, injection tests, audit trail, upload restrictions |
| 13 | Full Docker Compose, health checks, cloud deployment | Whole stack starts with one command |
| 14 | README, diagrams, demo, pre/post experiment, interview prep | Portfolio-ready repository |

## Milestones

- **M1 (end of Phase 5):** working non-agentic tutor app
- **M2 (end of Phase 7):** agentic workflow plus RAG
- **M3 (end of Phase 9):** the full learning loop
- **M4 (Phase 14):** everything in the specification

## Timeline estimate

Assumes 2 to 3 focused hours a day. Treat as roughly plus or minus 40 percent.

| Phases | Estimate |
|---|---|
| 1-2 | about 1 week |
| 3-5 | about 3 weeks |
| 6-7 | about 3 weeks |
| 8-9 | about 2 weeks |
| 10 | about 1.5 weeks |
| 11-12 | about 2 weeks |
| 13-14 | about 1.5 weeks |

Total: about 14 weeks.