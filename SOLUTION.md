# Task Manager API - Solution

**Status**: Phase 1 - Foundation (Config, Database, Backend-Frontend Communication)

---

## Architecture

### Planned Layered Structure

```
API Routes (Controllers)
    ↓
Services (Business Logic)
    ↓
Repositories (Data Access)
    ↓
SQLModel (ORM)
    ↓
PostgreSQL
```

**Current**: Foundation layer only (config, db, health check)

---

## What are Implemented

### Configuration (config.py)

Using Pydantic Settings for environment variable management:

- Reads from `.env` file (case-insensitive)
- Type-safe configuration
- Extra fields ignored (allows unused `.env` variables)

**Configuration Variables Defined**:

1. **Database Connection URL** (`database_url`)
   - PostgreSQL async connection string: `postgresql+asyncpg://user:pass@host:port/db`
   - Controls where the app connects to PostgreSQL
   - Can be overridden by environment variable

2. **JWT Secret Key** (`secret_key`)
   - Used for signing JWT tokens in authentication
   - Must be changed in production (currently: `dev-secret-key-change-in-production`)
   - Never commit production key to repository

3. **JWT Algorithm** (`algorithm`)
   - Algorithm for token signing: HS256 (HMAC with SHA-256)
   - sufficient for this scope

4. **CORS Origins** (`cors_origins`)
   - Comma-separated list of allowed frontend origins
   - Controls which domains can access the API
   - Default: `http://localhost:5173` (Vite dev server)

5. **Logging Configuration** (planned)
   - Not yet implemented
   - Future: Add log level, format, handlers

### Database Connection (db.py)

**Async Architecture** (SQLAlchemy + asyncpg):

- Non-blocking I/O for concurrent request handling
- Connection pooling: default 5 connections + 10 overflow
- Session lifecycle: `get_db()` dependency handles open/close automatically

**Configuration Details**:

1. **Engine Configuration**
   - `create_async_engine()`: Creates async engine (non-blocking)
   - `echo=False`: SQL queries not printed (set to True for debugging)
   - `future=True`: Uses SQLAlchemy 2.0+ style (modern, recommended)
   - **Why Async?**: FastAPI is async-native. Async DB operations prevent blocking the event loop, allowing high concurrency with low memory overhead

2. **Connection Pooling**
   - Default: 5 pre-allocated connections + 10 overflow connections under load
   - Reuses connections instead of creating new ones per request
   - Reduces database overhead and improves response time
   - Production-ready for current scope (configurable if needed)

3. **Session Lifecycle Management**
   - `get_db()`: FastAPI dependency that yields `AsyncSession`
   - `async with AsyncSessionLocal()`: Opens session
   - Automatic cleanup when request ends (context manager handles closing)
   - No manual `session.close()` needed
   - Testable: can override with mock sessions

4. **Base Model for SQLAlchemy Models**
   - `Base = declarative_base()`: Base class for all models
   - All User and Task models will inherit from `Base`
   - Tracks all table definitions for migrations/schema creation
   - Used by SQLModel to generate database tables

### Dependency Injection Pattern

Endpoints receive sessions via `Depends(get_db)`:

- FastAPI automatically injects `AsyncSession` to endpoints that request it
- Lifecycle: open session → endpoint runs → close session (automatic)
- Testable: can override `get_db` with mock sessions in tests
- No manual session creation/cleanup needed

### Health Check Endpoint

Verifies:

1. API is running
2. Database connection is active (executes `SELECT 1`)
3. Backend-Frontend communication works

---

## Requirements (From Challenge)

The following were specified in the challenge definition:

- JWT authentication (stateless, scalable)
- PostgreSQL + SQLAlchemy (specified in requirements)
- FastAPI (specified in requirements)
- Async support (challenge recommends async for scalability)

The architectural choice to support these:

- **Async design**: Better performance under concurrent load
- **Dependency Injection**: FastAPI best practice for session management

---

## Current Status

✅ Configuration working with environment variables  
✅ Database connection established and pooled  
✅ Health check verified database connectivity  
✅ CORS configured for frontend  
✅ Backend-Frontend communication tested

---

## Planned Next Steps

1. Define SQLModel models for User and Task
2. Implement Repository layer for data access
3. Implement Service layer for business logic
4. Add JWT authentication (login endpoint)
5. Create Task CRUD API endpoints
6. Add unit and integration tests

---

## Running

```bash
# Start database
docker compose up -d db

# Backend
uv run uvicorn src.main:app --reload

# Frontend
cd frontend && npm run dev

# Verify connection
curl http://localhost:8000/health
# Open http://localhost:5173 to see frontend call the backend
```

---

## Testing

### Run Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage report (terminal)
uv run pytest --cov=src

# Run tests with coverage report (HTML - full report)
uv run pytest --cov=src --cov-report=html

# View HTML coverage report
# Open htmlcov/index.html in your browser
```

### Coverage Configuration

Coverage is configured via `.coveragerc` for local development only:

- **Source**: `src/` directory
- **Excluded**: Tests, pycache, and virtual environments
- **HTML Report**: Generated in `htmlcov/` folder (interactive, per-file coverage details)
- **Terminal Report**: Quick summary in console

---

## Key Files

| File        | Purpose                                       |
| ----------- | --------------------------------------------- |
| `config.py` | Environment configuration                     |
| `db.py`     | Database engine & session management          |
| `main.py`   | FastAPI app (will be refactored with routers) |

This document will be updated as each phase is completed.
