from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies import get_test_service
from apps.soil_laboratory.schemas.test import (
    TestCreate,
    TestDetailResponse,
    TestListResponse, TestShortResponse
)
from apps.soil_laboratory.services.test import TestService


router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("/", response_model=TestListResponse)
async def get_tests_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    test_service: TestService = Depends(get_test_service),
    current_user: UserData = Depends(require_permission("tests.read"))
) -> TestListResponse:
    return await test_service.get_tests_paginated(page=page, per_page=per_page)


@router.post("/", response_model=TestDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_data: TestCreate,
    test_service: TestService = Depends(get_test_service),
    current_user: UserData = Depends(require_permission("tests.create"))
) -> TestDetailResponse:
    return await test_service.create_test(test_data)


@router.get("/{test_id:uuid}", response_model=TestDetailResponse)
async def get_test(
    test_id: UUID,
    test_service: TestService = Depends(get_test_service),
    current_user: UserData = Depends(require_permission("tests.read"))
) -> TestDetailResponse:
    return await test_service.get_test_by_id(test_id)


@router.delete("/{test_id}", response_model=TestShortResponse)
async def delete_test(
    test_id: UUID,
    test_service: TestService = Depends(get_test_service),
    current_user: UserData = Depends(require_permission("tests.delete"))
) -> TestShortResponse:
    return await test_service.delete_test(test_id)


# @router.post("/{test_id}/restore", response_model=TestDetailResponse)
# async def restore_test(
#     test_id: UUID,
#     test_service: TestService = Depends(get_test_service),
#     current_user: UserData = Depends(require_permission("tests.restore"))
# ) -> TestDetailResponse:
#     return await test_service.restore_test(test_id)
