# LinguaMate: Agentic AI Language Tutor

An AI-powered, personalised language tutor built with FastAPI, LangGraph, RAG and Streamlit.
The first release targets English learning for Indian learners, and the architecture is designed
so more languages can be added later.

> **Status: work in progress.** Phase 1 (project foundation) is the only phase built so far.
> Everything listed under "Planned features" does not exist yet.

## What works today

- FastAPI application skeleton with an application factory
- Typed, validated configuration loaded from environment variables
- `GET /health` endpoint with automatic Swagger documentation at `/docs`
- Automated tests with pytest

## Planned features

- Personalised learning planner and CEFR-based adaptive lessons
- Conversation tutor, grammar correction, vocabulary trainer with spaced repetition
- Quizzes with validated answer keys, reading and writing practice
- Speaking practice with speech-to-text, text-to-speech and pronunciation assessment
- LangGraph multi-step agent workflow with tools, memory and human-in-the-loop controls
- RAG over an educational knowledge base using Qdrant
- PostgreSQL persistence, Docker Compose deployment, evaluation suite

## Tech stack

Python, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, LangGraph, LangChain,
Qdrant, Sentence Transformers, Streamlit, Docker, Pytest.

## Quick start (Windows, Command Prompt)

```
git clone <repository-url>
cd linguamate
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
uvicorn linguamate.api.main:app --reload
```

Then open http://127.0.0.1:8000/docs in your browser.

Run the tests with:

```
pytest
```

## Project layout (current)

```
src/linguamate/   application package (core settings, api, schemas)
tests/            automated tests
pyproject.toml    project metadata and dependencies
.env.example      template for local settings (copy to .env)
```