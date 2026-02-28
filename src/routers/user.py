from fastapi import APIRouter, status, HTTPException, Depends
from uuid import UUID

from src.models import UserCreate, UserResponse, UserUpdate
from src.services.user_services import UserService
from src.dependencies import get_user_service

# Los objetos se llaman "routers"
router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """Register a new user"""
    try:
        return await service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
):
    """Get user by ID"""
    try:
        return await service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    """Update user information"""
    try:
        return await service.update_user(
            user_id, user_data.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        error_msg = str(e)
        if "user not found" in error_msg.lower():
            status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=status_code,
            detail=error_msg,
        )
