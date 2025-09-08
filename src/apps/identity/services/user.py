from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.models import User
from apps.identity.repositories import (
    PermissionRepository,
    RoleRepository,
    UserLoadOptions,
    UserRepository
)
from apps.identity.schemas import (
    UserCreate,
    UserDetailResponse,
    UserListItemResponse,
    UserListResponse,
    UserLookupResponse,
    UserShortResponse,
    UserUpdate
)
from core.exceptions.database import EntityNotFoundError, RelatedEntitiesNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria, SearchCriteria


class UserService:
    def __init__(
        self,
        db: AsyncSession,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        permission_repo: PermissionRepository
    ):
        self.db = db
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.permission_repo = permission_repo

    async def get_user_by_id(self, user_id: UUID) -> UserDetailResponse:
        user = await self.user_repo.get_by_id(
            user_id,
            include=[UserLoadOptions.ROLES, UserLoadOptions.PERMISSIONS, ]
        )

        if not user:
            raise EntityNotFoundError(user, user_id)

        return UserDetailResponse.model_validate(user)

    async def get_user_lookup_options(
        self,
        limit: int = 75,
        offset: int = 0,
        search: str | None = None
    ) -> list[UserLookupResponse]:
        user_entities = await self.user_repo.get_for_lookup(
            PaginationCriteria(limit, offset),
            SearchCriteria(search, User.email),
            OrderCriteria(User.email)
        )
        response_items = [UserLookupResponse.model_validate(user) for user in user_entities]

        return response_items

    async def get_users_paginated(self, page: int, per_page: int) -> UserListResponse:
        total_users = await self.user_repo.get_count(
            where_conditions=[User.deleted_at == None, ]
        )
        total_pages = max((total_users + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        user_entities = await self.user_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=[User.deleted_at == None, ],
            include=[UserLoadOptions.ROLES, UserLoadOptions.PERMISSIONS, ]
        )
        response_items = [UserListItemResponse.model_validate(user) for user in user_entities]

        return UserListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_users,
        )

    async def create_user(self, user_data: UserCreate) -> UserDetailResponse:
        user = await self.user_repo.create(user_data.to_dto())
        await self.db.flush()
        await self.db.refresh(user, attribute_names=["roles", "permissions"])

        if user_data.role_ids is not None:
            await self._set_user_roles(user, user_data.role_ids)

        if user_data.permission_ids is not None:
            await self._set_user_permissions(user, user_data.permission_ids)

        await self.db.commit()

        return await self.get_user_by_id(user.id)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserDetailResponse:
        user = await self.user_repo.update(user_id, user_data.to_dto())

        if not user:
            raise EntityNotFoundError(User, user_id)

        await self.db.refresh(user, attribute_names=["roles", "permissions"])

        if user_data.role_ids is not None:
            await self._set_user_roles(user, user_data.role_ids)

        if user_data.permission_ids is not None:
            await self._set_user_permissions(user, user_data.permission_ids)

        await self.db.commit()

        return await self.get_user_by_id(user.id)

    async def delete_user(self, user_id: UUID) -> UserDetailResponse:
        deleted_user = await self.user_repo.soft_delete(user_id)

        if not deleted_user:
            raise EntityNotFoundError(User, user_id)

        await self.db.commit()

        return await self.get_user_by_id(user_id)

    async def restore_user(self, user_id: UUID) -> UserDetailResponse:
        restored_user = await self.user_repo.restore(user_id)

        if not restored_user:
            raise EntityNotFoundError(User, user_id)

        await self.db.commit()

        return await self.get_user_by_id(user_id)

    async def _set_user_roles(
        self,
        user: User,
        role_ids: list[UUID]
    ) -> None:
        if not role_ids:
            user.roles = []
            return

        requested_ids = set(role_ids)
        roles = await self.role_repo.get_many_by_ids(list(requested_ids))

        if len(roles) != len(requested_ids):
            found_ids = {role.id for role in roles}
            missing_ids = requested_ids - found_ids

            raise RelatedEntitiesNotFoundError("Role", missing_ids)

        user.roles = roles

    async def _set_user_permissions(
        self,
        user: User,
        permission_ids: list[UUID]
    ) -> None:
        if not permission_ids:
            user.permissions = []
            return

        requested_ids = set(permission_ids)
        permissions = await self.permission_repo.get_many_by_ids(list(requested_ids))

        if len(permissions) != len(requested_ids):
            found_ids = {perm.id for perm in permissions}
            missing_ids = requested_ids - found_ids

            raise RelatedEntitiesNotFoundError("Permission", missing_ids)

        user.permissions = permissions
