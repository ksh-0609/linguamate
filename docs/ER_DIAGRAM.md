# Database ER Diagram

> **Planned schema.** No tables exist yet. They are created in Phase 2 with Alembic migrations.
> GitHub renders the diagram below automatically.

```mermaid
erDiagram
    LANGUAGES ||--o{ LEARNING_PROFILES : "target language"
    LANGUAGES ||--o{ LESSONS : "taught in"
    LANGUAGES ||--o{ VOCABULARY_ITEMS : "belongs to"
    USERS ||--|| LEARNING_PROFILES : "has"
    USERS ||--o{ STUDY_SESSIONS : "starts"
    STUDY_SESSIONS ||--o{ CONVERSATIONS : "includes"
    USERS ||--o{ CONVERSATIONS : "owns"
    CONVERSATIONS ||--o{ MESSAGES : "contains"
    USERS ||--o{ LESSON_PROGRESS : "completes"
    LESSONS ||--o{ LESSON_PROGRESS : "tracked in"
    GRAMMAR_TOPICS ||--o{ LESSONS : "taught by"
    GRAMMAR_TOPICS ||--o{ GRAMMAR_ERRORS : "classifies"
    USERS ||--o{ GRAMMAR_ERRORS : "makes"
    MESSAGES |o--o{ GRAMMAR_ERRORS : "source of"
    VOCABULARY_ITEMS ||--o{ USER_VOCABULARY : "learned as"
    USERS ||--o{ USER_VOCABULARY : "saves"
    USERS ||--o{ QUIZZES : "takes"
    QUIZZES ||--o{ QUIZ_QUESTIONS : "has"
    QUIZZES ||--o{ QUIZ_ATTEMPTS : "attempted in"
    USERS ||--o{ QUIZ_ATTEMPTS : "makes"
    QUIZ_ATTEMPTS ||--o{ QUIZ_ANSWERS : "records"
    QUIZ_QUESTIONS ||--o{ QUIZ_ANSWERS : "answered by"
    USERS ||--o{ SKILL_SNAPSHOTS : "measured by"
    USERS ||--o{ REVISION_SCHEDULES : "has due"
    USER_VOCABULARY |o--o{ REVISION_SCHEDULES : "scheduled"
    GRAMMAR_TOPICS |o--o{ REVISION_SCHEDULES : "scheduled"
    LESSONS |o--o{ REVISION_SCHEDULES : "scheduled"
    USERS ||--o{ AGENT_RUNS : "triggers"

    USERS {
        uuid id PK
        string email UK
        string password_hash
        bool is_active
        timestamp created_at
    }
    LEARNING_PROFILES {
        uuid id PK
        uuid user_id FK
        string native_language
        string target_language FK
        string cefr_level
        int daily_minutes
        json interests
    }
    USER_VOCABULARY {
        uuid id PK
        uuid user_id FK
        uuid vocab_item_id FK
        float ease_factor
        int interval_days
        int repetitions
        timestamp due_at
        string status
    }
    QUIZ_QUESTIONS {
        uuid id PK
        uuid quiz_id FK
        string question_type
        text prompt
        json options
        text answer_key
        string validation_status
    }
    REVISION_SCHEDULES {
        uuid id PK
        uuid user_id FK
        string item_type
        uuid user_vocabulary_id FK
        uuid grammar_topic_id FK
        uuid lesson_id FK
        timestamp due_at
    }
    AGENT_RUNS {
        uuid id PK
        uuid user_id FK
        string thread_id
        string intent
        string status
        int tokens_in
        int tokens_out
        int latency_ms
    }
```

## Design notes

- 19 tables. "Learning progress" is split into `lesson_progress` and `skill_snapshots`
  so each table has a single meaning.
- `vocabulary_items` holds shared word facts. `user_vocabulary` holds each learner's
  spaced-repetition state (ease factor, interval, due date).
- `revision_schedules` has three optional foreign keys. A CHECK constraint will require
  exactly one of them to be set, which avoids an un-normalised "polymorphic" column.
- `grammar_topics` links mistakes to lessons, so "recommend a relevant grammar lesson"
  becomes a deterministic lookup.
- `agent_runs` is the audit and evaluation trail: intent, tokens, latency, status.
- LangGraph's Postgres checkpointer creates its own tables separately.