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
1. _Week 1_: Directory restructure, FastAPI skeleton, health-check green.
2. _Week 2_: Database models & migrations; core engine compiles.
3. _Week 3_: API routes, first happy-path e2e test; Capacitor app scaffold.
4. _Week 4_: Authentication, currency subsystem verification; Capacitor UI for story start/view.
5. _Week 5_: CI pipeline, documentation polish, beta release to TestFlight / Play Console.

## 7. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| OpenAI rate limits | Blocks narrative generation | Implement exponential backoff & caching; allow fallback completion provider. |
| Mobile storage limits | Story tree may grow | Paginate older nodes to server; compress JSON. |
| Import path regressions | Runtime errors | Introduce `pytest` import test after each move. |
| Windows path quirks | Dev friction | Use `pathlib.Path` throughout; CI verifies on Ubuntu runner too. |

---
**Next step**: create folder skeleton & move files as indicated. Tick each item above as it completes.
