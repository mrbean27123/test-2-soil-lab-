from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_login, require_superuser
from apps.identity.dependencies.services import get_role_service
from apps.identity.schemas import (
    RoleCreate,
    RoleDetailResponse,
    RolePaginatedListResponse,
    RoleUpdate,
    UserData
)
from apps.identity.services import RoleService


router = APIRouter(prefix="/roles", tags=["roles"])


@router.get(
    "/lookups",
    response_model=RolePaginatedListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a paginated list of role lookups"
)
async def get_role_lookups_list(
    # Pagination
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number"),
    page_size: int = Query(
        10,
        ge=1,
        le=50,
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
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_login())
) -> RolePaginatedListResponse:
    return await role_service.get_roles_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )


@router.get(
    "/",
    response_model=RolePaginatedListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a paginated list of roles"
)
async def get_roles_list(
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
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RolePaginatedListResponse:
    return await role_service.get_roles_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )


@router.post("/", response_model=RoleDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RoleDetailResponse:
    return await role_service.create_role(role_data)


@router.get("/{role_id}", response_model=RoleDetailResponse)
async def get_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RoleDetailResponse:
    return await role_service.get_role_by_id(role_id)


@router.put("/{role_id}", response_model=RoleDetailResponse)
async def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RoleDetailResponse:
    return await role_service.update_role(role_id, role_data)


@router.delete("/{role_id}", response_model=RoleDetailResponse)
async def delete_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RoleDetailResponse:
    return await role_service.delete_role(role_id)


@router.post("/{role_id}/restore", response_model=RoleDetailResponse)
async def restore_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RoleDetailResponse:
    return await role_service.restore_role(role_id)
