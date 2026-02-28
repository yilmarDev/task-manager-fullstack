from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.models import Task, TaskStatus


class TaskRepository:
    """Data access layer for Task operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_task_by_id(self, task_id: UUID) -> Task | None:
        """Get a single task by ID"""
        return await self.db.get(Task, task_id)

    async def get_tasks_by_owner(self, owner_id: UUID) -> list[Task]:
        """Get all tasks owned by a user"""
        query = select(Task).where(Task.owner_id == owner_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_tasks_by_status(
        self, owner_id: UUID, status: TaskStatus
    ) -> list[Task]:
        """Get tasks by owner and status"""
        status_value = status.value if isinstance(status, TaskStatus) else status
        query = select(Task).where(
            (Task.owner_id == owner_id) & (Task.status == status_value)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_tasks_assigned_to(self, user_id: UUID) -> list[Task]:
        """Get tasks assigned to a specific user"""
        query = select(Task).where(Task.assigned_to_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_task(self, task: Task) -> Task:
        """Create and save a new Task"""
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task(self, task_id: UUID, task_data: dict) -> Task | None:
        """Update an existing task"""
        task = await self.get_task_by_id(task_id)
        if not task:
            raise ValueError("User not found")

        for key, value in task_data.items():
            if value is not None:
                setattr(task, key, value)

        task.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: UUID) -> bool:
        """Delete a task by ID"""
        task = await self.get_task_by_id(task_id)
        if not task:
            raise ValueError("User not found")

        await self.db.delete(task)
        await self.db.commit()
        return True
