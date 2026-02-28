from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.db import get_db, create_db_and_tables
from src.routers.user import router as users_router
from src.routers.task import router as tasks_router
from src.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - create tables on startup"""
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown
    pass


app = FastAPI(title="Task Manager API", lifespan=lifespan)

# Configure CORS from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)


# TODO: Implement your API
# Consider:
# - Authentication endpoints
# - Task CRUD operations
# - Project management
# - Permission checking
# - Health check endpoint


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    # error = True
    # if error:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="Fail Getting data"
    #     )
    return {"message": "Task Manager API is working right now"}


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_db)):
    """Health check endpoint to verify API and database connection"""
    try:
        # Import here to avoid circular dependency
        from sqlalchemy import text

        # Test database connection
        await session.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "service": "Task Manager API",
            "database": "connected",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Task Manager API",
            "database": f"disconnected - {str(e)}",
        }
