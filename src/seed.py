from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import User
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService

logger = logging.getLogger(__name__)


async def seed_demo_admin(session: AsyncSession) -> None:
    """Create demo admin (owner) and member users if configured.

    This runs at startup (lifespan) and is fully internal: no HTTP endpoint
    is exposed for creating users.
    """

    # Safety guard: only seed when explicitly enabled
    if not settings.seed_demo_data:
        return

    repo = UserRepository(session)
    service = UserService(repo)

    # --- Admin (owner) ---
    if not settings.demo_admin_password:
        logger.warning(
            "SEED_DEMO_DATA is enabled but DEMO_ADMIN_PASSWORD is not set; "
            "skipping demo admin creation."
        )
    else:
        existing_admin = await repo.get_user_by_email(settings.demo_admin_email)
        if existing_admin:
            logger.info(
                "Demo admin user with email %s already exists; skipping.",
                settings.demo_admin_email,
            )
        else:
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

    # --- Member ---
    if not settings.demo_member_password:
        logger.warning(
            "SEED_DEMO_DATA is enabled but DEMO_MEMBER_PASSWORD is not set; "
            "skipping demo member creation."
        )
        return

    existing_member = await repo.get_user_by_email(settings.demo_member_email)
    if existing_member:
        logger.info(
            "Demo member user with email %s already exists; skipping.",
            settings.demo_member_email,
        )
        return

    member_user = User(
        name="Demo Member",
        email=settings.demo_member_email,
        password_hash=service.hash_password(settings.demo_member_password),
        role="member",
    )
    await repo.create_user(member_user)
    logger.info(
        "Demo member user created with email %s and role 'member'",
        settings.demo_member_email,
    )
