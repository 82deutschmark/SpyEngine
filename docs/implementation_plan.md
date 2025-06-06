# Implementation Plan

This document outlines the concrete steps required to refactor the salvaged Spy Engine backend, prepare a clean API for a CapacitorJS mobile front-end, and harden the project for long-term maintenance by future developers.

---
## 1. Project Goals
1. **Stabilise the existing Python backend** without rewriting core business logic.
2. **Expose a versioned REST API** (FastAPI) that the CapacitorJS client can consume.
3. **Prepare a front-end skeleton** using CapacitorJS so that the same codebase deploys to iOS, Android, and the web.
4. **Introduce repeatable DevOps workflows** (virtual-env, `.env`, Alembic migrations, GitHub Actions, Docker-Compose dev stack).

## 2. Directory Structure (final target)
```text
SpyEngine/
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py           # FastAPI factory
│  │  ├─ api/
│  │  │  └─ v1/endpoints.py    # /story , /choice , /state …
│  │  ├─ core/                 # orchestrators (game_engine etc.)
│  │  ├─ services/             # story_maker, segment_maker …
│  │  ├─ models/               # SQLAlchemy models
│  │  ├─ utils/                # constants, currency_utils …
│  │  ├─ db/                   # engine + Alembic migrations
│  │  └─ settings.py           # Pydantic-based config loader
│  └─ tests/
├─ frontend/
│  └─ capacitor-app/           # Ionic/React project root
├─ docs/
│  ├─ architecture.md          # high-level reference (see below)
│  └─ implementation_plan.md   # THIS file – use as checklist
└─ .env                         # secrets & local overrides
```

Folders will be created incrementally; stubs (`__init__.py` or `.gitkeep`) ensure Git tracks empty directories.

## 3. Backend Refactor Tasks
| # | Task | Details |
|---|------|---------|
| 3.1 | **Bootstrap FastAPI app** | Create `backend/app/__init__.py` with an app factory and health-check route. |
| 3.2 | **Re-home existing modules** | Move/rename: `game_engine.py` → `backend/app/core/game_engine.py`, `segment_maker.py` → `services/segment_maker.py`, etc. Update imports (e.g. `from utils.constants import …`). |
| 3.3 | **Models** | Translate `database_schema.md` into SQLAlchemy models under `backend/app/models`. |
| 3.4 | **Database setup** | Provide `db/__init__.py` that exposes `engine`, `SessionLocal`, and `Base`. Add Alembic config for migrations. |
| 3.5 | **Settings & .env** | Use Pydantic `BaseSettings` to load: `DATABASE_URL`, `OPENAI_API_KEY`, `DEFAULT_OPENAI_MODEL`, etc. |
| 3.6 | **API Layer** | Implement `/v1/story/new`, `/v1/story/{id}/choice`, `/v1/state`, `/v1/missions` endpoints returning JSON. |
| 3.7 | **Authentication** | Protect game routes with JWT Bearer tokens (PyJWT). |
| 3.8 | **Logging & Error Handling** | Standardise logging via `uvicorn` & Python `logging`. Provide exception middleware. |
| 3.9 | **Unit Tests** | Configure `pytest`, add smoke tests for each endpoint and core service. |
| 3.10 | **Docs & OpenAPI** | FastAPI auto-generates `/docs`. Ensure response models (`pydantic`) are accurate. |

## 4. Front-end Tasks (CapacitorJS)
| # | Task | Details |
|---|------|---------|
| 4.1 | **Initialise Ionic/Capacitor project** inside `frontend/capacitor-app` (React or Vue – dev preference). |
| 4.2 | **Environment config** | Store API base URL in Capacitor Config & `.env`. |
| 4.3 | **Pages** |    * Home / StorySetup<br> * StoryView (scrollable narrative)<br> * ChoicePicker<br> * Missions<br> * Settings/Login |
| 4.4 | **API Client** | Lightweight wrapper around `fetch` or Axios with JWT attachment and error interceptors. |
| 4.5 | **State Persistence** | Use Capacitor Storage to cache current `GameState` for offline play. |
| 4.6 | **Build & Deploy** | `npx cap build android` / `ios`. Verify live reload via `npx cap run`. |

## 5. DevOps & Tooling
1. **Python** ≥ 3.11 – pin versions in `backend/requirements.txt`.
2. **Pre-commit hooks**: black, isort, flake8.
3. **GitHub Actions**: lint, tests, build Capacitor web artefact, optionally open-api diff.
4. **Docker Compose**: service graph – `backend`, `postgres`, optional `nginx`.

## 6. Milestones
1. # of prompts needed???  : Directory restructure, FastAPI skeleton, health-check green.
2.  # of prompts needed??? : Database models & migrations; core engine compiles.
3. # of prompts needed??? : API routes, first happy-path e2e test; Capacitor app scaffold.
4. # of prompts needed??? : Authentication, currency subsystem verification; Capacitor UI for story start/view.
5. # of prompts needed??? : CI pipeline, documentation polish, beta release to TestFlight / Play Console.

## 7. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| OpenAI rate limits | Blocks narrative generation | Implement exponential backoff & caching; allow fallback completion provider. LOW PRIORITY |
| Mobile storage limits | Story tree may grow | Paginate older nodes to server; compress JSON. LOW PRIORITY |
| Import path regressions | Runtime errors | Introduce `pytest` import test after each move. |
| Windows path quirks | Dev friction | Use `pathlib.Path` throughout; CI verifies on Ubuntu runner too. |

---
**Next step**: create folder skeleton & move files as indicated. Tick each item above as it completes.

---
## 8. Progress Log

**Update: June 6, 2025 (Handoff from Cascade AI Assistant)**

**Summary of Work:**

*   **Directory Structure & File Placement (Task 3.1 partially, related to 3.2):**
    *   Backend directory structure under `backend/app/` created with `__init__.py` files.
    *   Key modules moved/confirmed: `game_engine.py` (core), `segment_maker.py` (services - DEPRECATED), `story_maker.py` (services), `state_manager.py` (services), `game_api.py` (api/v1), utils (`constants.py`, `currency_utils.py`, `db_utils.py`), `character_data.py` (models), `mission_generator.py` (services), `character_interaction.py` (services - unimplemented).

*   **Import Statement Updates (Task 3.2 - In Progress):**
    *   `backend/app/core/game_engine.py`: Updated to relative imports. `CharacterInteractionService` import commented out. Unused `generate_continuation` import removed.
    *   `backend/app/services/story_maker.py`: Updated to relative imports. Imports for missing `character_evolution.py` and `validation_utils.py` commented out.
    *   `backend/app/services/segment_maker.py`: Reviewed. Module is DEPRECATED. No internal import changes made.

*   **Status of Previously Missing Files:**
    *   `character_data.py`: Now at `backend/app/models/character_data.py`.
    *   `mission_generator.py`: Now at `backend/app/services/mission_generator.py`.
    *   `character_interaction.py`: Now at `backend/app/services/character_interaction.py` (unimplemented).
    *   `character_evolution.py`: **Still MISSING** (expected in `backend/app/services/`).
    *   `validation_utils.py`: **Still MISSING** (expected in `backend/app/utils/`).

**Notes for Next Developer:**

*   **Continue Import Updates (Task 3.2):** Focus on `backend/app/api/v1/game_api.py` (Flask to FastAPI refactor & relative imports). Check utils.
*   **Address Missing Files:** Locate/create `character_evolution.py` and `validation_utils.py`.
*   **Database Integration (Task 3.4):** Implement SQLAlchemy setup in `backend/app/db/__init__.py`.
*   **API Layer Refactor (Task 3.6):** Refactor `game_api.py` from Flask to FastAPI.
*   **Deprecated `segment_maker.py`:** Plan for eventual removal.
*   **Code Comments:** Use "Gemini 2.5 Pro" and current date for new work.
