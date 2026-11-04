# LinguaMate Architecture

> **Target architecture.** Only the FastAPI skeleton (settings, `/health`, tests) exists today.
> See `PROJECT_STATUS.md` for what is actually built.

## System overview

```
┌──────────────┐   HTTP/JSON    ┌─────────────────────────────────────┐
│  Streamlit   │ ─────────────► │  FastAPI  (routers → services)      │
│  frontend    │ ◄───────────── │  auth · validation · rate limiting  │
└──────────────┘                └──────────────┬──────────────────────┘
                                               │ calls
                         ┌─────────────────────┼──────────────────────┐
                         ▼                     ▼                      ▼
                 ┌───────────────┐   ┌───────────────────┐   ┌───────────────┐
                 │ Domain        │   │ LangGraph agent   │   │ Speech        │
                 │ services      │◄──│ graph + tools     │   │ STT/TTS/pron. │
                 │ (deterministic│   │ (router, nodes,   │   └───────────────┘
                 │  business     │   │  memory, limits)  │
                 │  logic)       │   └────────┬──────────┘
                 └──────┬────────┘            │
                        │                     ├──► LLM factory (Gemini/OpenAI/Ollama)
                        ▼                     └──► RAG (embed → Qdrant → rerank)
                 ┌───────────────┐                      │
                 │ PostgreSQL    │                      ▼
                 │ (SQLAlchemy + │              ┌───────────────┐
                 │  Alembic)     │              │ Qdrant        │
                 └───────────────┘              └───────────────┘
```

## Design principles

1. Endpoints never contain LLM logic. They call a service, and the service calls the agent
   graph or the LLM layer.
2. Plain Python decides everything deterministic (auth, scoring, scheduling, validation).
   The LLM decides only what needs language understanding.
3. Agent tools wrap tested services, validate input and output, and only touch the current
   user's data. No tool exposes raw SQL or code execution.
4. The LLM provider is chosen by configuration (`LLM_PROVIDER`), not by code changes.

## Technology stack

| Layer | Choice | Why |
|---|---|---|
| API | FastAPI + Pydantic | Automatic Swagger docs, built-in validation |
| Database | PostgreSQL, SQLAlchemy, Alembic | Relational integrity, versioned migrations |
| Agents | LangGraph | Explicit state, conditional edges, checkpointing, human-in-the-loop |
| LLM access | LangChain chat model from a provider factory | Provider-agnostic without a custom abstraction |
| Default LLM | Gemini free tier (Ollama optional) | Zero cost for the MVP |
| Embeddings | Local Sentence Transformers | Free, no API calls |
| Vector DB | Qdrant | Metadata filtering and hybrid search |
| Reranking | Cross-encoder | Cheap precision boost on top-K results |
| Speech-to-text | faster-whisper (local) | Free; transcription only |
| TTS and pronunciation | Azure Speech free tier | Real pronunciation assessment, separate from transcription |
| Frontend | Streamlit | Fast route to a professional UI in Python |
| Testing | Pytest | Standard |
| Packaging | Docker, Docker Compose | Reproducible deployment |

## Directory structure

Phase 1 created: `src/linguamate/{__init__, core, schemas, api}` and `tests/`.
Everything else below is planned and will be created in its own phase.

```
linguamate/
├── .env.example
├── .gitignore
├── README.md
├── PROJECT_STATUS.md
├── pyproject.toml
├── docker-compose.yml
├── alembic.ini
├── alembic/versions/
├── docker/                 # api.Dockerfile, frontend.Dockerfile
├── data/
│   ├── knowledge_base/     # grammar, vocabulary and reading source files
│   └── eval_sets/          # CEFR-level test datasets
├── src/linguamate/
│   ├── core/               # config, logging, security, errors
│   ├── db/                 # base, session, models/, repositories/
│   ├── schemas/            # Pydantic request and response models
│   ├── api/                # main.py, deps.py, routers/
│   ├── services/           # business logic (spaced repetition, scoring, planner rules)
│   ├── llm/                # provider factory, structured output, usage tracking
│   ├── prompts/            # versioned prompt templates
│   ├── agents/             # state, graph, router, nodes/, tools/, guardrails
│   ├── rag/                # ingest, chunking, embeddings, store, retrieve, rerank
│   ├── speech/             # stt, tts, pronunciation, audio utils
│   └── evaluation/         # metrics and runners
├── frontend/               # app.py, pages/, components/, api_client.py
├── tests/                  # unit/, integration/, agents/, rag/, security/
└── docs/
```

## Agent workflow

```
START
  │
  ▼
[load_context]     deterministic: profile, level, weak topics, recent messages
  │
  ▼
[input_guard]      deterministic: size/format checks, injection patterns
  │  (blocked) ───────────────────────────────► [safe_refusal] ─► END
  ▼
[supervisor]       rules first; LLM (structured output) only if unclear
  │
  ├─► [conversation]  tools: retrieve_lesson_content, record_grammar_mistake
  ├─► [grammar]       tools: search_grammar_knowledge, record_grammar_mistake
  ├─► [vocabulary]    tools: save_vocabulary, schedule_revision
  ├─► [assessment]    tools: generate_quiz, calculate_quiz_score
  ├─► [planner]       tools: get_weak_topics, recommend_next_lesson
  └─► [analysis]      tools: get_learning_history, update_progress
  │
  ▼
[output_validator] deterministic: schema check, level check, retry (max 2)
  │
  ▼
[persist_trace]    deterministic: DB writes, token and latency logging
  │
  ▼
END
```

| The LLM decides | Plain Python decides |
|---|---|
| Intent, when rules do not match | Authentication and per-user authorization |
| Conversation replies | Schema and answer-key validation |
| Grammar error detection and explanation | Quiz scoring |
| Drafting quiz questions | Spaced-repetition schedule |
| Planner reasoning over candidates the code supplies | Streaks, stats, CEFR-change thresholds |
| Narrative progress summary | Rate limits, retries, tool permission checks, database writes |

**Human-in-the-loop:** LangGraph interrupts pause the workflow for learner approval of a new
study plan or a CEFR level change, and for review of a quiz whose answer key failed validation.

**Execution limits:** a maximum number of graph steps, a maximum number of tool calls per
request, per-call timeouts and capped retries.