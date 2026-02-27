from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.config import settings

# Base class for all SQLAlchemy models
Base = declarative_base()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL logging
    future=True,
)

# Session factory - use async_sessionmaker for async context manager support
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """Dependency to get database session in endpoints"""
    async with AsyncSessionLocal() as session:
        yield session
