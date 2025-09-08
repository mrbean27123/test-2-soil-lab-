from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_login, require_superuser
from apps.identity.dependencies.services import get_role_service
from apps.identity.schemas import (
    RoleCreate,
    RoleDetailResponse,
    RoleListResponse,
    RoleLookupResponse,
    RoleUpdate,
    UserData
)
from apps.identity.services import RoleService


router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/lookups", response_model=list[RoleLookupResponse])
async def get_role_lookups_list(
    limit: int | None = Query(75, ge=1, le=500),
    search: str | None = Query(None, min_length=2, max_length=50),
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_login())
) -> list[RoleLookupResponse]:
    return await role_service.get_role_lookup_options(limit=limit, search=search)


@router.get("/", response_model=RoleListResponse)
async def get_roles_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    role_service: RoleService = Depends(get_role_service),
    current_user: UserData = Depends(require_superuser())
) -> RoleListResponse:
    return await role_service.get_roles_paginated(page=page, per_page=per_page)


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
