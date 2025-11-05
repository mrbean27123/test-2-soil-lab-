from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.models import Permission
from apps.identity.repositories import PermissionRepository
from apps.identity.schemas import (
    PermissionCreate,
    PermissionDetailResponse,
    PermissionListItemResponse,
    PermissionPaginatedListResponse,
    PermissionUpdate
)
from apps.identity.specifications import (
    PaginationSpecification,
    PermissionFilterSpecification,
    PermissionOrderingSpecification,
    PermissionSearchSpecification
)
from core.exceptions.database import EntityNotFoundError


class PermissionService:
    def __init__(self, db: AsyncSession, permission_repo: PermissionRepository):
        self.db = db
        self.permission_repo = permission_repo

    async def get_permission_by_id(self, permission_id: UUID) -> PermissionDetailResponse:
        permission = await self.permission_repo.get_by_id(permission_id)

        if not permission:
            raise EntityNotFoundError(Permission, permission_id)

        return PermissionDetailResponse.model_validate(permission)

    # async def get_permission_lookup_options(
    #     self,
    #     page_number: int,
    #     page_size: int,
    #     ordering: str | None = None,
    #     q: str | None = None
    # ) -> PermissionPaginatedLookupListResponse:
    #     ...

    async def get_permissions_paginated(
        self,
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None
    ) -> PermissionPaginatedListResponse:
        pagination_spec = PaginationSpecification(page_number, page_size)
        ordering_spec = PermissionOrderingSpecification(ordering)
        filter_spec = PermissionFilterSpecification()
        search_spec = PermissionSearchSpecification(q)

        total_permissions = await self.permission_repo.get_count(filter_spec, search_spec)
        total_pages = pagination_spec.get_total_pages(total_permissions)

        permission_entities = await self.permission_repo.get_all_paginated(
            pagination_spec,
            ordering_spec,
            filter_spec,
            search_spec
        )
        response_items = [
            PermissionListItemResponse.model_validate(permission)
            for permission in permission_entities
        ]

        return PermissionPaginatedListResponse(
            data=response_items,
            page=page_number,
            total_pages=total_pages,
            total_items=total_permissions
        )

    async def create_permission(
        self,
        permission_data: PermissionCreate
    ) -> PermissionDetailResponse:
        permission = await self.permission_repo.create(permission_data.to_dto())

        await self.db.commit()

        return PermissionDetailResponse.model_validate(permission)

    async def update_permission(
        self,
        permission_id: UUID,
        permission_data: PermissionUpdate
    ) -> PermissionDetailResponse:
        permission = await self.permission_repo.update(permission_id, permission_data.to_dto())

        if not permission:
            raise EntityNotFoundError(Permission, permission_id)

        await self.db.commit()

        return await self.get_permission_by_id(permission_id)

    async def delete_permission(self, permission_id: UUID) -> PermissionDetailResponse:
        deleted_permission = await self.permission_repo.soft_archive(permission_id)

        if not deleted_permission:
            raise EntityNotFoundError(Permission, permission_id)

        await self.db.commit()

        return await self.get_permission_by_id(permission_id)

    async def restore_permission(self, permission_id: UUID) -> PermissionDetailResponse:
        restored_permission = await self.permission_repo.restore(permission_id)

        if not restored_permission:
            raise EntityNotFoundError(Permission, permission_id)

        await self.db.commit()

        return await self.get_permission_by_id(permission_id)
