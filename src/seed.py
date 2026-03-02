from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import User
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService

logger = logging.getLogger(__name__)


async def seed_demo_admin(session: AsyncSession) -> None:
    """Create a demo admin (owner) user if configured and not already present.

    This runs at startup (lifespan) and is fully internal: no HTTP endpoint
    is exposed for creating admin users.
    """

    # Safety guard: only seed when explicitly enabled
    if not settings.seed_demo_data:
        return

    # Require an explicit password from environment to avoid hardcoding secrets
    if not settings.demo_admin_password:
        logger.warning(
            "SEED_DEMO_DATA is enabled but DEMO_ADMIN_PASSWORD is not set; "
            "skipping demo admin creation."
        )
        return

    repo = UserRepository(session)

    # Idempotent: if the user already exists, do nothing
    existing = await repo.get_user_by_email(settings.demo_admin_email)
    if existing:
        logger.info(
            "Demo admin user with email %s already exists; skipping seeding.",
            settings.demo_admin_email,
        )
        return

    service = UserService(repo)

    admin_user = User(
        name="Demo Owner",
        email=settings.demo_admin_email,
        password_hash=service.hash_password(settings.demo_admin_password),
        role="owner",
    )

    await repo.create_user(admin_user)
    logger.info(
        "Demo admin user created with email %s and role 'owner'",
        settings.demo_admin_email,
    )
