# System Architecture Reference

> **Version:** 0.1 (2025-05-03)
>
> Use this document to orient new developers. Keep updated after each significant backend or mobile release.

---

## 1. Logical Architecture

```mermaid
graph TD
  subgraph Mobile App (CapacitorJS)
    APP[Spy Engine App]
  end
  subgraph API Edge (FastAPI)
    API[/api/v1/*/]
  end
  subgraph Domain Layer
    GE[Game Engine]
    SM[Story Maker]
    SEG[Segment Maker]
    MIS[Mission Generator]
    CI[Character Interaction]
  end
  subgraph Persistence
    PG[(PostgreSQL)]
  end
  subgraph External Services
    OA[[OpenAI GPT-4]]
  end
  APP -- HTTPS + JWT --> API
  API --> GE
  GE --> SM & SEG & MIS & CI
  SM & SEG --> OA
  GE --> PG
  CI --> PG
  MIS --> PG
```

### Description
* **Mobile App** – Capacitor-based iOS/Android/Web container running a React UI.
* **API Edge** – FastAPI application running behind `uvicorn`. Handles auth, validation, and marshals requests to domain.
* **Domain Layer** – Pure-Python services encapsulating business logic; stateless – no HTTP/context objects.
* **Persistence** – PostgreSQL accessed via SQLAlchemy ORM. Alembic migrations manage schema.
* **External Services** – OpenAI completions for dynamic narrative generation.

---

## 2. Module Mapping (post-refactor)

| Layer | Module | Path | Notes |
|-------|--------|------|-------|
| Utils | constants | `backend/app/utils/constants.py` | Centralised config – `CURRENCY_TYPES`, `EXCHANGE_RATES`, OpenAI defaults. |
| Utils | currency_utils | `backend/app/utils/currency_utils.py` | Ledger, validation, conversion – references `EXCHANGE_RATES`. |
| Core | GameEngine | `backend/app/core/game_engine.py` | Orchestrates story state, missions, and player economy. |
| Service | StoryMaker | `backend/app/services/story_maker.py` | Builds initial prompts; calls OpenAI. |
| Service | SegmentMaker | `backend/app/services/segment_maker.py` | Generates follow-up story nodes. |
| Service | MissionGenerator | `backend/app/services/mission_generator.py` | Creates & mutates mission objects. |
| Service | CharacterInteraction | `backend/app/services/character_interaction.py` | Handles dialogue and relationship stats. |
| Model | SQLAlchemy models | `backend/app/models/*` | `UserProgress`, `StoryNode`, `Character`, `Mission`, `Transaction`. |
| DB | session & base | `backend/app/db/__init__.py` | `SessionLocal`, `engine`, `Base`. |
| API | v1 endpoints | `backend/app/api/v1/endpoints.py` | Public contract consumed by Capacitor app. |

---

## 3. Key Data Structures

### 3.1 GameState
```jsonc
{
  "current_story_id": 123,
  "current_node_id": 456,
  "currency_balances": {
    "💎": 490,
    "💶": 5020,
    "💴": 150000,
    "💵": 4800,
    "💷": 5000
  },
  "active_missions": [12, 13],
  "choice_history": ["Investigate the ambassador", "Trust the informant"]
}
```

### 3.2 StoryNode
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | PK |
| `story_id` | int | FK → StoryGeneration |
| `parent_id` | int/null | FK self-ref |
| `text` | Text | Narrative paragraph |
| `branch_metadata` | JSON | Includes protagonist info, missions delta, encountered characters |
| `created_at` | ts | ─ |

---

## 4. Configuration & Env Vars
* `OPENAI_API_KEY` – secrets manager / `.env`.
* `DATABASE_URL` – `postgresql://user:pass@host/db`.
* `JWT_SECRET_KEY` – auth signing key.
* `DEFAULT_OPENAI_MODEL`, `DEFAULT_TEMPERATURE`, `DEFAULT_MAX_TOKENS` – **see** `utils/constants.py`.

---

## 5. Sequence Diagram – Choice Flow

```mermaid
sequenceDiagram
  participant App
  participant API
  participant GE
  participant SEG
  participant PG as DB
  App->>API: POST /story/456/choice {"choice": "Enter the vault"}
  API->>GE: make_choice(user_id, data)
  GE->>SEG: generate_continuation(context)
  SEG->>OpenAI: Completion(prompt)
  OpenAI-->>SEG: narrative + metadata
  SEG-->>GE: StoryNode
  GE->>PG: INSERT story_node, UPDATE state
  PG-->>GE: ack
  GE-->>API: JSON(new node, balances)
  API-->>App: 200 OK
```

---

## 6. Non-Functional Highlights
* **Scalability** – Runtime is stateless; replicate API pods horizontally. Cache currency rates.
* **Observability** – JSON logs, `metrics/` endpoint, OpenAI latency histogram.
* **Security** – All endpoints behind HTTPS; JWT expiry 30 min; refresh tokens.
* **Resilience** – Database `READ COMMITTED`; OpenAI calls wrapped in backoff + circuit breaker.

---

## 7. Glossary
| Term | Meaning |
|------|---------|
| **CapacitorJS** | A runtime that packages web code into native Android/iOS containers with plugin access. |
| **StoryGeneration** | A root object describing the initial prompt parameters (conflict, setting, style, mood). |
| **StoryNode** | A single narrative block plus branching metadata. |
| **Mission** | A player objective yielding currency/XP on completion. |
| **Transaction** | Immutable ledger record for any currency change. |

---

_Last updated: 2025-05-03_
