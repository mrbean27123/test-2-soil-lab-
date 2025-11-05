from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.identity.models import Permission
from repositories.base import (
    ArchiveByStatusMixin,
    BaseRepository,
    CreateMixin,
    ExistsMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    UpdateMixin
)


class PermissionLoadOptions(str, Enum):
    USERS = "users"


class PermissionRepository(
    BaseRepository[Permission, PermissionLoadOptions],
    ExistsMixin[Permission],
    ReadPaginatedMixin[Permission, PermissionLoadOptions],
    ReadByIdMixin[Permission, PermissionLoadOptions],
    CreateMixin[Permission],
    UpdateMixin[Permission],
    ArchiveByStatusMixin[Permission]
):
    _LOAD_OPTIONS_MAP: dict[PermissionLoadOptions, Load] = {
        PermissionLoadOptions.USERS: selectinload(Permission.users)
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Permission)
