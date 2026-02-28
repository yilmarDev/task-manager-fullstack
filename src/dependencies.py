from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService
from src.repositories.task_repository import TaskRepository
from src.services.task_services import TaskService


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
