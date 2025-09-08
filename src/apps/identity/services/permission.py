from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.models import Permission
from apps.identity.repositories import PermissionRepository
from apps.identity.schemas import (
    PermissionCreate,
    PermissionDetailResponse,
    PermissionListItemResponse,
    PermissionListResponse,
    PermissionLookupResponse,
    PermissionUpdate
)
from core.exceptions.database import EntityNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria, SearchCriteria


class PermissionService:
    def __init__(self, db: AsyncSession, permission_repo: PermissionRepository):
        self.db = db
        self.permission_repo = permission_repo

    async def get_permission_by_id(self, permission_id: UUID) -> PermissionDetailResponse:
        permission = await self.permission_repo.get_by_id(permission_id)

        if not permission:
            raise EntityNotFoundError(Permission, permission_id)

        return PermissionDetailResponse.model_validate(permission)

    async def get_permission_lookup_options(
        self,
        limit: int = 100,
        offset: int = 0,
        search: str | None = None
    ) -> list[PermissionLookupResponse]:
        permission_entities = await self.permission_repo.get_for_lookup(
            PaginationCriteria(limit, offset),
            SearchCriteria(search, Permission.name),
            OrderCriteria(Permission.name)
        )
        response_items = [
            PermissionLookupResponse.model_validate(permission)
            for permission in permission_entities
        ]

        return response_items

    async def get_permissions_paginated(self, page: int, per_page: int) -> PermissionListResponse:
        total_permissions = await self.permission_repo.get_count(
            where_conditions=[Permission.archived_at == None, ]
        )
        total_pages = max((total_permissions + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        permission_entities = await self.permission_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=[Permission.archived_at == None, ]
        )
        response_items = [
            PermissionListItemResponse.model_validate(permission)
            for permission in permission_entities
        ]

        return PermissionListResponse(
            data=response_items,
            page=page,
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
