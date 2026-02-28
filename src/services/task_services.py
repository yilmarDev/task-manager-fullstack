from uuid import UUID
from datetime import datetime, timezone

from src.models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskStatus, User
from src.repositories.task_repository import TaskRepository


class TaskService:
    """Business logic layer for Task operations"""

    def __init__(self, repository: TaskRepository):
        self.repo = repository

    async def create_task(self, owner_id: UUID, task_data: TaskCreate) -> TaskResponse:
        """Create a new task"""
        if task_data.assigned_to_id:
            assigned_user = await self.repo.db.get(User, task_data.assigned_to_id)
            if not assigned_user:
                raise ValueError(
                    f"Assigned user not found"
                )

        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            owner_id=owner_id,
            assigned_to_id=task_data.assigned_to_id,
            status=TaskStatus.PENDING,
        )

        created_task = await self.repo.create_task(task)
        return TaskResponse.model_validate(created_task)

    async def get_task(self, task_id: UUID, user_id: UUID) -> TaskResponse:
        """Get a task with permission check"""
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        # Check if user is owner or assigned to the task
        if task.owner_id != user_id and task.assigned_to_id != user_id:
            raise PermissionError("You don't have permission to view this task")

        return TaskResponse.model_validate(task)

    async def list_user_tasks(
        self, user_id: UUID, status: TaskStatus | None = None
    ) -> list[TaskResponse]:
        """List tasks owned by user, optionally filtered by status"""
        if status:
            tasks = await self.repo.get_tasks_by_status(user_id, status)
        else:
            tasks = await self.repo.get_tasks_by_owner(user_id)

        return [TaskResponse.model_validate(task) for task in tasks]

    async def list_assigned_tasks(self, user_id: UUID) -> list[TaskResponse]:
        """List tasks assigned to user"""
        tasks = await self.repo.get_tasks_assigned_to(user_id)

        return [TaskResponse.model_validate(task) for task in tasks]

    async def update_task(
        self, task_id: UUID, user_id: UUID, task_data: dict
    ) -> TaskResponse:
        """Update a task with permission check"""
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task not found")

        if task.owner_id != user_id:
            raise PermissionError("Only the task owner can update this task")

        # # Build update dict excluding None values
        # update_dict = {
        #     k: v for k, v in task_data.model_dump().items() if v is not None
        # }

        updated_task = await self.repo.update_task(task_id, task_data)
        return TaskResponse.model_validate(updated_task)

    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a task with permission check"""
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        if task.owner_id != user_id:
            raise PermissionError("Only the task owner can delete this task")

        return await self.repo.delete_task(task_id)
