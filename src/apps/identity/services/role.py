from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.models import Role
from apps.identity.repositories import PermissionRepository, RoleLoadOptions, RoleRepository
from apps.identity.schemas import (
    RoleCreate,
    RoleDetailResponse,
    RoleListItemResponse,
    RoleListResponse,
    RoleLookupResponse,
    RoleShortResponse,
    RoleUpdate
)
from core.exceptions.database import EntityNotFoundError, RelatedEntitiesNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria, SearchCriteria


class RoleService:
    def __init__(
        self,
        db: AsyncSession,
        role_repo: RoleRepository,
        permission_repo: PermissionRepository
    ):
        self.db = db
        self.role_repo = role_repo
        self.permission_repo = permission_repo

    async def get_role_by_id(self, role_id: UUID) -> RoleDetailResponse:
        role = await self.role_repo.get_by_id(
            role_id,
            include=[RoleLoadOptions.PERMISSIONS, ]
        )

        if not role:
            raise EntityNotFoundError(Role, role_id)

        return RoleDetailResponse.model_validate(role)

    async def get_role_lookup_options(
        self,
        limit: int = 50,
        offset: int = 0,
        search: str | None = None
    ) -> list[RoleLookupResponse]:
        role_entities = await self.role_repo.get_for_lookup(
            PaginationCriteria(limit, offset),
            SearchCriteria(search, Role.name),
            OrderCriteria(Role.name)
        )
        response_items = [RoleLookupResponse.model_validate(role) for role in role_entities]

        return response_items

    async def get_roles_paginated(self, page: int, per_page: int) -> RoleListResponse:
        total_roles = await self.role_repo.get_count(
            where_conditions=[Role.archived_at == None, ]
        )
        total_pages = max((total_roles + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        role_entities = await self.role_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=[Role.archived_at == None, ],
            include=[RoleLoadOptions.PERMISSIONS, ]
        )
        response_items = [RoleListItemResponse.model_validate(role) for role in role_entities]

        return RoleListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_roles
        )

    async def create_role(self, role_data: RoleCreate) -> RoleDetailResponse:
        role = await self.role_repo.create(role_data.to_dto())

        if role_data.permission_ids is not None:
            await self.db.flush()
            await self.db.refresh(role, attribute_names=["permissions"])

            await self._set_role_permissions(role, role_data.permission_ids)

        await self.db.commit()

        return RoleDetailResponse.model_validate(role)

    async def update_role(self, role_id: UUID, role_data: RoleUpdate) -> RoleDetailResponse:
        role = await self.role_repo.update(role_id, role_data.to_dto())

        if not role:
            raise EntityNotFoundError(Role, role_id)

        if role_data.permission_ids is not None:
            await self.db.refresh(role, attribute_names=["permissions"])

            await self._set_role_permissions(role, role_data.permission_ids)

        await self.db.commit()

        return await self.get_role_by_id(role_id)

    async def delete_role(self, role_id: UUID) -> RoleDetailResponse:
        deleted_role = await self.role_repo.soft_archive(role_id)

        if not deleted_role:
            raise EntityNotFoundError(Role, role_id)

        await self.db.commit()

        return await self.get_role_by_id(role_id)

    async def restore_role(self, role_id: UUID) -> RoleDetailResponse:
        restored_role = await self.role_repo.restore(role_id)

        if not restored_role:
            raise EntityNotFoundError(Role, role_id)

        await self.db.commit()

        return await self.get_role_by_id(role_id)

    async def _set_role_permissions(
        self,
        role: Role,
        permission_ids: list[UUID]
    ) -> None:
        if not permission_ids:
            role.permissions = []
            return

        requested_ids = set(permission_ids)
        permissions = await self.permission_repo.get_many_by_ids(list(requested_ids))

        if len(permissions) != len(requested_ids):
            found_ids = {perm.id for perm in permissions}
            missing_ids = requested_ids - found_ids

            raise RelatedEntitiesNotFoundError("Permission", missing_ids)

        role.permissions = permissions
