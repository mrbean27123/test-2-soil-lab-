from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_login, require_superuser
from apps.identity.dependencies.services import get_user_service
from apps.identity.schemas import (
    UserCreate,
    UserData,
    UserDetailResponse,
    UserListResponse,
    UserLookupResponse, UserUpdate
)
from apps.identity.services import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/lookups", response_model=list[UserLookupResponse])
async def get_user_lookups_list(
    limit: int | None = Query(75, ge=1, le=500),
    search: str | None = Query(None, min_length=2, max_length=50),
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_login())
) -> list[UserLookupResponse]:
    return await user_service.get_user_lookup_options(limit=limit, search=search)


@router.get("/", response_model=UserListResponse)
async def get_users_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserListResponse:
    return await user_service.get_users_paginated(page=page, per_page=per_page)


@router.post("/", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserDetailResponse:
    return await user_service.create_user(user_data)


@router.get("/me", response_model=UserDetailResponse)
async def get_me(
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_login())
) -> UserDetailResponse:
    return await user_service.get_user_by_id(current_user.id)


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserDetailResponse:
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserDetailResponse:
    return await user_service.update_user(user_id, user_data)


@router.delete("/{user_id}", response_model=UserDetailResponse)
async def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserDetailResponse:
    return await user_service.delete_user(user_id)


@router.post("/{user_id}/restore", response_model=UserDetailResponse)
async def restore_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserDetailResponse:
    return await user_service.restore_user(user_id)
