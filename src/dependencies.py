from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService
from src.db import get_db


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Factory: Provide UserRepository"""
    return UserRepository(db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Factory: Provide UserService"""
    return UserService(repo)
