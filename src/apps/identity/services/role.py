from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.models import Role
from apps.identity.repositories import PermissionRepository, RoleLoadOptions, RoleRepository
from apps.identity.schemas import (
    RoleCreate,
    RoleDetailResponse,
    RoleListItemResponse,
    RolePaginatedListResponse,
    RoleUpdate
)
from apps.identity.specifications import (
    PaginationSpecification,
    RoleFilterSpecification,
    RoleOrderingSpecification,
    RoleSearchSpecification
)
from core.exceptions.database import EntityNotFoundError, RelatedEntitiesNotFoundError


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
        role = await self.role_repo.get_by_id(role_id, include=[RoleLoadOptions.PERMISSIONS, ])

        if not role:
            raise EntityNotFoundError(Role, role_id)

        return RoleDetailResponse.model_validate(role)

    # async def get_role_lookup_options(
    #     self,
    #     page_number: int,
    #     page_size: int,
    #     ordering: str | None = None,
    #     q: str | None = None
    # ) -> RolePaginatedLookupListResponse:
    #     ...

    async def get_roles_paginated(
        self,
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None
    ) -> RolePaginatedListResponse:
        pagination_spec = PaginationSpecification(page_number, page_size)
        ordering_spec = RoleOrderingSpecification(ordering)
        filter_spec = RoleFilterSpecification()
        search_spec = RoleSearchSpecification(q)

        total_roles = await self.role_repo.get_count(filter_spec, search_spec)
        total_pages = pagination_spec.get_total_pages(total_roles)

        role_entities = await self.role_repo.get_all_paginated(
            pagination_spec,
            ordering_spec,
            filter_spec,
            search_spec,
            include=[RoleLoadOptions.PERMISSIONS, ]
        )
        response_items = [RoleListItemResponse.model_validate(role) for role in role_entities]

        return RolePaginatedListResponse(
            data=response_items,
            page=page_number,
            total_pages=total_pages,
            total_items=total_roles
        )

    async def create_role(self, role_data: RoleCreate) -> RoleDetailResponse:
        role = await self.role_repo.create(role_data.to_dto())

        if role_data.permission_ids is not None:
            await self.db.refresh(role, attribute_names=["permissions"])
            await self._set_role_permissions(role, role_data.permission_ids)

        await self.db.commit()

        return await self.get_role_by_id(role.id)

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

    async def _set_role_permissions(self, role: Role, permission_ids: list[UUID]) -> None:
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
