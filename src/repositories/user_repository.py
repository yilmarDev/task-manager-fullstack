from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlmodel import select

from src.models import User


class UserRepository:
    """Data access layer for User operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        """Get user by email"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID"""
        return await self.db.get(User, user_id)

    async def create_user(self, user: User) -> User:
        """Create and save a new User"""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: UUID, user_data: dict) -> User:
        """Update existing user"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
