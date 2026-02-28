from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.config import settings
from src.models import UserResponse
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService
from src.repositories.task_repository import TaskRepository
from src.services.task_services import TaskService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Factory: Provide UserRepository"""
    return UserRepository(db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Factory: Provide UserService"""
    return UserService(repo)


def get_task_repository(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    """Factory: Provide TaskRepository"""
    return TaskRepository(db)


def get_task_service(
    repo: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    """Factory: Provide TaskService"""
    return TaskService(repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Dependency: Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        user_id = UUID(user_id_str)
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception

    try:
        user = await user_service.get_user(user_id)
        if user is None:
            raise credentials_exception
        return user
    except ValueError:
        raise credentials_exception
