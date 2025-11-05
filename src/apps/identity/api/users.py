from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_login, require_superuser
from apps.identity.dependencies.services import get_user_service
from apps.identity.schemas import (
    UserCreate,
    UserData,
    UserDetailResponse,
    UserPaginatedListResponse,
    UserUpdate
)
from apps.identity.services import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=UserPaginatedListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a paginated list of users"
)
async def get_users_list(
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
    user_service: UserService = Depends(get_user_service),
    current_user: UserData = Depends(require_superuser())
) -> UserPaginatedListResponse:
    return await user_service.get_users_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )


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
