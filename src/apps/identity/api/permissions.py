from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_login, require_superuser
from apps.identity.dependencies.services import get_permission_service
from apps.identity.schemas import (
    PermissionCreate,
    PermissionDetailResponse,
    PermissionListResponse,
    PermissionLookupResponse,
    PermissionUpdate,
    UserData
)
from apps.identity.services import PermissionService


router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/lookups", response_model=list[PermissionLookupResponse])
async def get_permission_lookups_list(
    limit: int | None = Query(75, ge=1, le=500),
    search: str | None = Query(None, min_length=2, max_length=50),
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_login())
) -> list[PermissionLookupResponse]:
    return await permission_service.get_permission_lookup_options(limit=limit, search=search)


@router.get("/", response_model=PermissionListResponse)
async def get_permissions_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionListResponse:
    return await permission_service.get_permissions_paginated(page=page, per_page=per_page)


@router.post("/", response_model=PermissionDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionDetailResponse:
    return await permission_service.create_permission(permission_data)


@router.get("/{permission_id}", response_model=PermissionDetailResponse)
async def get_permission(
    permission_id: UUID,
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionDetailResponse:
    return await permission_service.get_permission_by_id(permission_id)


@router.put("/{permission_id}", response_model=PermissionDetailResponse)
async def update_permission(
    permission_id: UUID,
    permission_data: PermissionUpdate,
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionDetailResponse:
    return await permission_service.update_permission(permission_id, permission_data)


@router.delete("/{permission_id}", response_model=PermissionDetailResponse)
async def delete_permission(
    permission_id: UUID,
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionDetailResponse:
    return await permission_service.delete_permission(permission_id)


@router.post("/{permission_id}/restore", response_model=PermissionDetailResponse)
async def restore_permission(
    permission_id: UUID,
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionDetailResponse:
    return await permission_service.restore_permission(permission_id)
