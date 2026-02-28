from fastapi import APIRouter, status, HTTPException, Depends
from uuid import UUID

from src.models import TaskCreate, TaskResponse, TaskUpdate, TaskStatus, UserResponse
from src.services.task_services import TaskService
from src.dependencies import get_task_service, get_current_user

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: UserResponse = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Create a new task"""
    try:
        return await service.create_task(current_user.id, task_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/assigned", response_model=list[TaskResponse])
async def list_assigned_tasks(
    current_user: UserResponse = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """List tasks assigned to user"""
    return await service.list_assigned_tasks(current_user.id)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    status: TaskStatus | None = None,
    current_user: UserResponse = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """List user's tasks with optional status filter"""
    return await service.list_user_tasks(current_user.id, status)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Get a task by ID"""
    try:
        return await service.get_task(task_id, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: UserResponse = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Update a task"""
    try:
        return await service.update_task(
            task_id, current_user.id, task_data.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Delete a task"""
    try:
        await service.delete_task(task_id, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
