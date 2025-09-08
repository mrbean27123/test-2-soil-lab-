from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.repositories import (
    PermissionRepository,
    RoleRepository,
    TokenRepository,
    UserRepository
)
from database.dependencies import get_postgresql_db_session as get_db_session


def get_token_repository(db: AsyncSession = Depends(get_db_session)) -> TokenRepository:
    return TokenRepository(db)


def get_permission_repository(db: AsyncSession = Depends(get_db_session)) -> PermissionRepository:
    return PermissionRepository(db)


def get_role_repository(db: AsyncSession = Depends(get_db_session)) -> RoleRepository:
    return RoleRepository(db)


def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)
