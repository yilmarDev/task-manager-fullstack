docker compose up --build
docker compose up -d db

# Task Manager API - Solution

**Status**: MVP implemented (auth, tasks, frontend, Docker) with focus on clean architecture and DX for reviewers.

---

## High-Level Architecture

The system is structured in layers to keep concerns separated and testable:

```
API Routers (FastAPI controllers)
      ↓
Services (business logic)
      ↓
Repositories (data access)
      ↓
SQLModel models (ORM)
      ↓
PostgreSQL
```

- Routers live in `src/routers` (auth, users, tasks) and only handle HTTP concerns.
- Services in `src/services` contain the business rules (auth, validation, permissions).
- Repositories in `src/repositories` encapsulate all SQL/ORM access.
- Models in `src/models.py` are SQLModel entities and response/request schemas.

This separation lets me:

- Unit-test services independently of FastAPI and the database.
- Swap the persistence layer (e.g. another DB) without touching controllers.
- Keep controllers very thin and focused on HTTP status codes and error mapping.

---

## Backend Design

### Configuration (`src/config.py`)

I use **Pydantic Settings** to centralize configuration:

- Reads from `.env` (case-insensitive, extra fields ignored).
- Typed fields for DB URL, JWT settings, CORS, and demo-mode seeding.

Main settings:

1. **Database URLs**
   - `database_url`: used by the async engine in local development
     (for example: `postgresql+asyncpg://<db_user>:<db_password>@localhost:5432/<db_name>`).
   - `DOCKER_DATABASE_URL` (via env): used only in Docker, where the host is `db`.

2. **JWT Configuration**
   - `secret_key`: signing key (default dev value, must be overridden in real envs).
   - `algorithm`: HS256.
   - `access_token_expire_minutes`: configurable token lifetime.

3. **CORS**
   - `cors_origins`: comma-separated origins (e.g. `http://localhost:5173`).
   - In `src/main.py` it is split and passed to `CORSMiddleware`.

4. **Demo / seeding mode**
   - `seed_demo_data: bool`: feature-flag for demo seed.
   - `demo_admin_email`, `demo_admin_password`.
   - `demo_member_email`, `demo_member_password`.
   - All passwords are provided via environment variables (no real secrets in Git).

This design keeps secrets and environment-specific values out of code and aligns with the TODOs in the starter (`database URL`, `JWT`, `CORS`).

### Async Database Layer (`src/db.py`)

The database layer is fully **async** using SQLAlchemy 2.x + `asyncpg`:

- `create_async_engine(settings.database_url, future=True, echo=False)` creates a non-blocking engine.
- `AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)` is the session factory.
- `get_db()` is a FastAPI dependency which `yield`s an `AsyncSession` inside an `async with` block.

**Why async everywhere?**

- FastAPI is designed around `async` endpoints; using blocking DB calls would limit concurrency.
- Async DB operations free the event loop while waiting on I/O, allowing the same process to serve many concurrent requests.
- The pattern scales both locally and inside Docker without changing code.

### Models and Relationships (`src/models.py`)

I use **SQLModel** to define both DB tables and Pydantic-like schemas:

- `User` and `Task` are `SQLModel, table=True` entities.
- `Task` has relationships to `User`:
  - `owner_id` and `assigned_to_id` foreign keys.
  - `owner` and `assigned_to` relationships configured with `lazy="selectin"`.

Using `lazy="selectin"` tells SQLAlchemy to fetch related `User` rows in efficient batches instead of one query per task. This avoids the classic N+1 problem when returning lists of tasks that include their owners and assignees.

Response models implement a **Backend-for-Frontend** style:

- `TaskDetailResponse` includes embedded `UserSummary` for owner and assignee.
- This avoids multiple round-trips from the frontend and keeps the API tailored to UI needs.

### Repositories and Services

**Repositories** (`src/repositories/*.py`):

- `UserRepository` exposes methods like `get_user_by_email`, `get_all_users`, `create_user`, `update_user`.
- `TaskRepository` encapsulates list/creation/update/delete of tasks and assigned tasks for a user.

**Services** (`src/services/*.py`):

- `UserService` handles:
  - Password hashing and verification (via `passlib` + bcrypt).
  - User registration with email uniqueness checks.
  - Authentication (`authenticate_user`) used by the auth router.
  - Business rules for updating users (e.g. avoiding duplicate emails).
- `TaskService` encapsulates the rules around who can create, assign and update tasks.

This design matches the requirement for “production-ready” code:

- Controllers stay small and declarative.
- Business rules are centralized and testable.
- Data access is abstracted, making future refactors easier.

### Dependency Injection (`src/dependencies.py`)

To comply with the **Dependency Inversion Principle** (SOLID), I centralize wiring in `dependencies.py`:

- `get_user_service(db: AsyncSession)` builds a `UserService` from a `UserRepository`.
- `get_task_service(db: AsyncSession)` does the same for tasks.
- `get_current_user` decodes the JWT, loads the `User` and exposes a `UserResponse` to routers.

Routers depend only on **abstractions** (services), not on concrete DB details. For tests, these dependencies can be overridden to inject fakes or in-memory DBs.

### Authentication and Security

- I use **PyJWT** (`pyjwt`) to sign and verify access tokens in `src/core/security.py`.
- The login endpoint (`src/routers/auth.py`) implements the standard OAuth2 password flow:
  - Expects `username` and `password` form fields.
  - Delegates to `UserService.authenticate_user`.
  - On success, returns a JWT with `sub = user.id` and an `exp` claim based on `access_token_expire_minutes`.
- Protected endpoints depend on `get_current_user`, which:
  - Extracts the `Authorization: Bearer` token.
  - Decodes and validates it with the configured `secret_key` and `algorithm`.
  - Loads the user and enforces role-based rules (e.g. only `owner` can list all users).

This approach keeps the JWT logic small, explicit and testable, while using a widely adopted library with good community support.

### Lifespan and Demo Seeding (`src/main.py`, `src/seed.py`)

I use FastAPI's **lifespan** to run one-time startup tasks:

- On startup:
  - `create_db_and_tables()` creates all SQLModel tables (idempotent).
  - If `settings.seed_demo_data` is `True`, I open an `AsyncSession` and call `seed_demo_admin(session)`.

`seed_demo_admin` in `src/seed.py`:

- Reads demo credentials from settings:
  - `DEMO_ADMIN_EMAIL`, `DEMO_ADMIN_PASSWORD`.
  - `DEMO_MEMBER_EMAIL`, `DEMO_MEMBER_PASSWORD`.
- Creates two users **only if they don't already exist**:
  - An `owner` user (admin) with role `"owner"`.
  - A second `member` user with role `"member"`.
- Passwords are hashed using the same logic as regular registration.
- If passwords are not configured, the seeding for that user is skipped with a log message.

Security considerations:

- There is **no HTTP endpoint** like "/create-admin"; all seeding is internal and guarded by env vars.
- This allows a recruiter to get ready-to-use demo users without exposing backdoors.

### Testing and Coverage

- Tests live in `tests/` and are run with `pytest` / `pytest-asyncio` for async support.
- I added `pytest-cov` to measure coverage:
  - Terminal report: quick overview of covered lines.
  - HTML report (`htmlcov/index.html`): detailed per-file coverage.
- Fixtures in `tests/conftest.py` provide isolated DB sessions and HTTP clients so that tests are deterministic and fast.

This meets the requirement of “production-readiness” by ensuring critical flows (auth, tasks) are covered.

---

## Frontend Design

### Stack and Libraries

The frontend is built with **React + Vite** and a modern UI/tooling stack:

- **React Router** (`react-router-dom`) for routing between `/login`, `/tasks` and `/status`.
- **TanStack Query** for data fetching/caching (`useCurrentUserQuery`, `useAsignedTasksQuery`).
- **react-hook-form** + **zod** for form handling and validation on the login form.
- **Tailwind CSS** and **shadcn/ui** for consistent, accessible UI components.
- UI layout initially prototyped with v0 and then integrated manually.

### Pages and Flow

- `LoginPage`:
  - Checks `localStorage` for a JWT and its expiry (`isTokenExpired`).
  - If valid, automatically redirects to `/tasks`.
  - Otherwise shows the login form.
- `TasksPage` (dashboard):
  - Uses `useCurrentUserQuery` to fetch the current user based on the JWT `sub`.
  - Uses `useAsignedTasksQuery` to fetch assigned tasks.
  - On 401 or auth errors, redirects back to `/login` and relies on the logout helper to clear token and cache.
  - Shows stats cards and a filtered task list; tasks can be created and assigned to users.

The frontend calls the backend through a single Axios client:

- `VITE_API_BASE_URL` is set to `http://localhost:8000/api` (both locally and in Docker).
- All service functions use **relative paths** (e.g. `auth/login`, `users`, `tasks/assigned`).
- This guarantees that requests go to the `/api/...` prefixed endpoints defined in the FastAPI routers.

### Auth Integration

- On successful login, the access token is stored under `Authorization` in `localStorage`.
- All requests include `Authorization: Bearer <token>` via an Axios interceptor.
- Token utilities (`token.ts`) handle decoding, expiry checks and user id extraction.

This keeps auth concerns centralized and makes it easy to plug in a different storage or token format in the future.

---

## Docker & Developer Experience

### Original vs. Final Setup

The starter repository only dockerized **PostgreSQL** and the **FastAPI API**. I extended this to:

- Add a dedicated `frontend` service that runs the Vite dev server.
- Introduce env-based DB URLs so that credentials are not hardcoded in `docker-compose.yml`.
- Align CORS and `VITE_API_BASE_URL` so that the browser → frontend → backend path works consistently.

### Current `docker-compose.yml`

Services:

- `db` (Postgres 18):
  - Uses `DB_USER`, `DB_PASSWORD`, `DB_NAME` from `.env` with sane defaults.
  - Healthcheck with `pg_isready`.
  - Data persisted in the named volume `postgres_data`.

- `backend` (FastAPI):
  - Built from the root `Dockerfile` using Python 3.13 and `uv` for dependency management.
  - Reads `DATABASE_URL` from `DOCKER_DATABASE_URL` so the host is `db` inside the Docker network.
  - Inherits `SECRET_KEY`, `ALGORITHM`, `CORS_ORIGINS` from `.env` (no secrets hardcoded in Compose).
  - Exposes port `8000`.

- `frontend` (React + Vite):
  - Built from `frontend/Dockerfile` on top of `node:20-alpine`.
  - Serves the Vite dev server on port `5173` with `--host` so it is reachable from the host.
  - Receives `VITE_API_BASE_URL=http://localhost:8000/api` from Compose, aligning with backend routes.

### Quick Start for Reviewers

From the project root:

```bash
cp .env.example .env
docker compose up --build
```

Then:

- Frontend: http://localhost:5173
- API root: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

This matches the “Definition of Done” asking for a project that can be started easily and reproducibly.

## Environment & Configuration

The repository includes a `.env.example` file documenting all important settings. In practice there are three main groups:

- Backend database & app config
  - `DB_USER`, `DB_PASSWORD`, `DB_NAME`: used by `docker-compose` to create the Postgres user/database.
  - `DATABASE_URL`: connection string used when running the backend directly on the host.
  - `DOCKER_DATABASE_URL`: connection string used by the backend container (host is `db` inside the Docker network).
  - `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`: control JWT signing and token lifetime.
  - `CORS_ORIGINS`: comma-separated list of allowed browser origins (e.g. `http://localhost:5173`).

- Demo mode
  - `SEED_DEMO_DATA`: enables/disables creation of demo users at startup.
  - `DEMO_ADMIN_EMAIL`, `DEMO_ADMIN_PASSWORD`: credentials for the seeded owner user.
  - `DEMO_MEMBER_EMAIL`, `DEMO_MEMBER_PASSWORD`: credentials for the seeded member user.

- Frontend
  - `VITE_API_BASE_URL`: base URL for Axios. In Docker it is set via `docker-compose` to `http://localhost:8000/api`; when running the frontend without Docker it should still point to the same backend root.

For reviewers the minimal setup is copying `.env.example` to `.env` and filling in `SECRET_KEY` and the demo passwords; the other values have sensible defaults for local `docker compose up`.

---

## Demo Mode and Seed Users

To make the evaluation smoother, I added a **demo mode** controlled entirely by environment variables, without exposing any insecure endpoints.

### How it Works

- In `.env.example` I document:
  - `SEED_DEMO_DATA=true`
  - `DEMO_ADMIN_EMAIL`, `DEMO_ADMIN_PASSWORD` (owner user).
  - `DEMO_MEMBER_EMAIL`, `DEMO_MEMBER_PASSWORD` (member user).
- In `src/main.py`, the lifespan hook calls `seed_demo_admin` only when `SEED_DEMO_DATA` is enabled.
- The seeder:
  - Creates the owner user with role `owner` if it does not exist.
  - Creates a second user with role `member` if it does not exist.
  - Is **idempotent**: re-running the app does not duplicate users.

This allows reviewers to:

1. Log in as the owner.
2. Create and assign tasks to the member user.

…without having to manually create users or run SQL scripts.

### Security Rationale

- No `/create-admin` or similar HTTP route exists.
- All seeding is internal, triggered only when explicitly configured via environment variables.
- Passwords are never hardcoded in the repo; each user of the project chooses their own demo passwords in `.env`.

---

## Testing & Coverage

Tests are run with:

```bash
uv run pytest tests/ -v
```

Coverage:

```bash
uv run pytest --cov=src
uv run pytest --cov=src --cov-report=html  # htmlcov/index.html
```

- Coverage is configured to focus on `src/`.
- HTML report provides detailed, per-file coverage to identify gaps.

The most critical flows (auth, user permissions, task operations) are covered; in this solution coverage for the `src` package stays above 90%, which matches typical "production-ready" expectations.

## Stretch Goals

Some features go beyond the bare minimum of the exercise:

- Full async stack (FastAPI + async SQLModel + async tests) instead of a sync demo.
- Dockerized frontend service so reviewers only need `docker compose up --build`.
- Role-based access control (owner vs member) and APIs tailored to the dashboard (assigned tasks endpoint, embedded owner/assignee info).
- Demo mode with seeded owner/member users driven entirely by environment variables.
- Test suite with coverage reporting to validate the most important flows.

There are also stretch ideas intentionally left as future work:

- Comments or activity log on tasks so teams can see history.
- Real-time notifications or websockets for task updates.
- More advanced filtering/sorting on the frontend.
- Exposing the full update/delete flow for tasks in the UI (the backend already supports it).

---

## Trade-offs and Possible Improvements

- **Alembic vs. SQLModel create_all**: I chose `SQLModel.metadata.create_all` for schema management to keep the solution lightweight. For a real product, I would introduce Alembic migrations and possibly data migrations for seeding.
- **Single backend service**: Everything runs in one FastAPI app. With more time, I would consider extracting background jobs (e.g. notifications) into separate workers.
- **Frontend state management**: React Query covers server state. For a larger app I might introduce a client-state solution (Zustand, Redux Toolkit) but it felt unnecessary for this scope.
- **Logging and observability**: Logging is minimal; next steps would be structured logging, request IDs and better error categorization.
- **Auth token storage**: Right now JWTs are stored in `localStorage`. For a hardened production deployment I would move tokens to HttpOnly cookies with CSRF protection.
- **OAuth providers**: With more time I would plug in OAuth (e.g. Google/GitHub) on top of the existing JWT infrastructure.
- **Task lifecycle & audit**: Soft delete for tasks and richer audit trails would make the system safer in real teams.
- **Task management UI**: The backend already exposes update/delete operations; wiring those into the frontend would complete the CRUD experience.

Within the timebox I prioritized: (1) a solid auth/role model and a smooth owner→member flow; (2) an end‑to‑end Docker developer experience; and (3) reliable tests/coverage for core flows. Nice-to-have UI polish and secondary features were left for future iterations.

Overall, the goal was to deliver a small but coherent system: layered backend, modern frontend, full Docker setup, and a smooth reviewer experience.
