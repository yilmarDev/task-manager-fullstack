from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4, UUID

from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime


class TaskStatus(str, Enum):
    """Enumeration for task status values"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class User(SQLModel, table=True):
    """Database model for User"""

    __table_args__ = {"extend_existing": True}

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="member")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


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
    updated_at: datetime


class Task(SQLModel, table=True):
    """Database model for Task"""

    __table_args__ = {"extend_existing": True}

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default=TaskStatus.PENDING.value, index=True)
    owner_id: UUID = Field(foreign_key="user.id", index=True)
    assigned_to_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    due_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


class TaskCreate(SQLModel):
    """Schema for creating a task (request)"""

    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[UUID] = None


class TaskUpdate(SQLModel):
    """Schema for updating a task (request)"""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[datetime] = None


class TaskResponse(SQLModel):
    """Schema for task response"""

    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    owner_id: UUID
    assigned_to_id: Optional[UUID]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
