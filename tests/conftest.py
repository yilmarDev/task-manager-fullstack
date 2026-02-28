import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from uuid import uuid4

from src.main import app
from src.db import get_db
from src.models import SQLModel, User


# Test database URL - use SQLite in-memory for fast tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_db_session(test_db_engine):
    """Create test database session"""
    AsyncSessionLocal = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def client(test_db_session):
    """Create test client with dependency override"""

    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db_session):
    """Create a test user in the database"""
    from src.services.user_services import UserService
    from src.repositories.user_repository import UserRepository

    repo = UserRepository(test_db_session)
    service = UserService(repo)

    user = User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password_hash=service.hash_password("testpass123"),
        role="member",
    )

    created_user = await repo.create_user(user)
    return created_user


@pytest.fixture
async def test_task(test_db_session, test_user):
    """Create a test task in the database"""
    from src.models import Task, TaskStatus

    task = Task(
        id=uuid4(),
        title="Test Task",
        description="This is a test task",
        status=TaskStatus.PENDING,
        owner_id=test_user.id,
        assigned_to_id=None,
    )

    test_db_session.add(task)
    await test_db_session.commit()
    await test_db_session.refresh(task)
    return task
