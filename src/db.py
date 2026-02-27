from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from src.config import settings

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


async def create_db_and_tables():
    """Create all database tables using SQLModel metadata"""
    # Import models here to register them with SQLModel
    from src.models import User  # noqa: F401

    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️  Warning: Could not create database tables: {e}")
        print("Make sure PostgreSQL is running and accessible.")


async def get_db():
    """Dependency to get database session in endpoints"""
    async with AsyncSessionLocal() as session:
        yield session
