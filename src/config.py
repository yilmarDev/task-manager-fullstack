from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env"""

    # Database
    database_url: str = (
        "postgresql+asyncpg://taskuser:taskpass@localhost:5432/taskmanager"
    )

    # JWT
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from .env (such as db_user, db_password, db_name)
    )


settings = Settings()
