from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_login, require_superuser
from apps.identity.dependencies.services import get_permission_service
from apps.identity.schemas import (
    PermissionCreate,
    PermissionDetailResponse,
    PermissionPaginatedListResponse,
    PermissionUpdate,
    UserData
)
from apps.identity.services import PermissionService


router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get(
    "/lookups",
    response_model=PermissionPaginatedListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a paginated list of permission lookups"
)
async def get_permission_lookups_list(
    # Pagination
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number"),
    page_size: int = Query(
        10,
        ge=1,
        le=100,
        alias="page[size]",
        description="Number of items per page"
    ),
    # Ordering & Search
    ordering: str | None = Query(
        None,
        description="Ordering field (prefix with '-' for descending)"
    ),
    q: str | None = Query(None, description="Full-text search query across main searchable fields"),
    # Dependencies
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_login())
) -> PermissionPaginatedListResponse:
    return await permission_service.get_permissions_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )


@router.get(
    "/",
    response_model=PermissionPaginatedListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a paginated list of permissions"
)
async def get_permissions_list(
    # Pagination
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number"),
    page_size: int = Query(
        10,
        ge=1,
        le=20,
        alias="page[size]",
        description="Number of items per page"
    ),
    # Ordering & Search
    ordering: str | None = Query(
        None,
        description="Ordering field (prefix with '-' for descending)"
    ),
    q: str | None = Query(None, description="Full-text search query across main searchable fields"),
    # Dependencies
    permission_service: PermissionService = Depends(get_permission_service),
    current_user: UserData = Depends(require_superuser())
) -> PermissionPaginatedListResponse:
    return await permission_service.get_permissions_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )


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
