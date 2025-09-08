from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.identity.models import Role
from repositories.base import (
    ArchiveByStatusMixin,
    BaseRepository,
    CountMixin,
    CreateMixin,
    ExistsMixin,
    LookupMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    UpdateMixin
)


class RoleLoadOptions(str, Enum):
    PERMISSIONS = "permissions"
    USERS = "users"


class RoleRepository(
    BaseRepository[Role, RoleLoadOptions],
    ExistsMixin[Role],
    CountMixin[Role],
    LookupMixin[Role],
    ReadPaginatedMixin[Role, RoleLoadOptions],
    ReadByIdMixin[Role, RoleLoadOptions],
    CreateMixin[Role],
    UpdateMixin[Role],
    ArchiveByStatusMixin[Role]
):
    _LOAD_OPTIONS_MAP: dict[RoleLoadOptions, Load] = {
        RoleLoadOptions.PERMISSIONS: selectinload(Role.permissions),
        RoleLoadOptions.USERS: selectinload(Role.users)
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Role)
