from enum import Enum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.identity.dto import UserCreateDTO
from apps.identity.models import User
from repositories.base import (
    BaseRepository,
    CreateMixin,
    ExistsMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    SoftDeleteMixin,
    UpdateMixin
)


class UserLoadOptions(str, Enum):
    ROLES = "roles"
    PERMISSIONS = "permissions"

    REFRESH_TOKENS = "refresh_tokens"


class UserRepository(
    BaseRepository[User, UserLoadOptions],
    ExistsMixin[User],
    ReadPaginatedMixin[User, UserLoadOptions],
    ReadByIdMixin[User, UserLoadOptions],
    CreateMixin[User],
    UpdateMixin[User],
    SoftDeleteMixin[User]
):
    _LOAD_OPTIONS_MAP: dict[UserLoadOptions, Load] = {
        UserLoadOptions.ROLES: selectinload(User.roles),
        UserLoadOptions.PERMISSIONS: selectinload(User.permissions),
        UserLoadOptions.REFRESH_TOKENS: (selectinload(User.refresh_tokens))
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def create(self, user_data: UserCreateDTO) -> User:
        user = User.create(**user_data.model_dump())
        self.db.add(user)

        return user

    async def get_by_email(
        self,
        email: str,
        include: list[UserLoadOptions] | None = None
    ) -> User | None:
        stmt = select(User).where(User.email == email)
        stmt = self._apply_load_options(stmt, include)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
