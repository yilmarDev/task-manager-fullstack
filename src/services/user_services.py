from uuid import UUID

from passlib.context import CryptContext
from src.models import UserCreate, UserResponse, User


from src.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Business logic layer for User operations"""

    def __init__(self, repository: UserRepository):
        self.repo = repository

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""

        existing_user = await self.repo.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=self.hash_password(user_data.password),
        )

        created_user = await self.repo.create_user(user)
        return UserResponse.model_validate(created_user)

    async def get_user(self, user_id: UUID) -> UserResponse:
        """Get user by id"""
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: UUID, user_data: dict) -> UserResponse:
        """Update user info"""
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if "email" in user_data and user_data["email"] != user.email:
            existing = await self.repo.get_user_by_email(user_data["email"])
            if existing:
                raise ValueError("Email already registered")

        # Convert "password" to "password_hash" if provided
        if "password" in user_data and user_data["password"] is not None:
            user_data["password_hash"] = self.hash_password(user_data.pop("password"))

        updated_user = await self.repo.update_user(user_id, user_data)
        return UserResponse.model_validate(updated_user)

    async def authenticate_user(self, email: str, password: str) -> UserResponse:
        """Authenticate user"""
        user = await self.repo.get_user_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        return UserResponse.model_validate(user)
