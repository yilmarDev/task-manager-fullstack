from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4, UUID

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Database model for User"""

    __table_args__ = {"extend_existing": True}

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="member")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(SQLModel):
    """Schema for creating a user (request)"""

    name: str
    email: str
    password: str


class UserUpdate(SQLModel):
    """Schema for updating a user (request)"""

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(SQLModel):
    """Schema for user response (no password hash)"""

    id: UUID
    name: str
    email: str
    role: str
    created_at: datetime
