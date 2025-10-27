from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from apps.identity.dependencies.auth import require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_test_result_service
from apps.soil_laboratory.schemas.test_result import (
    TestResultCreate,
    TestResultDetailResponse,
    TestResultPaginatedListResponse,
    TestResultShortResponse
)
from apps.soil_laboratory.services.test_result import TestResultService


router = APIRouter(prefix="/test-results", tags=["test-results"])


@router.get("/", response_model=TestResultPaginatedListResponse)
async def get_tests_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    test_result_service: TestResultService = Depends(get_test_result_service),
    current_user: UserData = Depends(require_permission("test_results.read"))
) -> TestResultPaginatedListResponse:
    return await test_result_service.get_tests_paginated(page, per_page)


@router.post("/", response_model=TestResultDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_result_data: TestResultCreate,
    test_result_service: TestResultService = Depends(get_test_result_service),
    current_user: UserData = Depends(require_permission("test_results.create"))
) -> TestResultDetailResponse:
    return await test_result_service.create_test(test_result_data)


@router.get("/{test_result_id:uuid}", response_model=TestResultDetailResponse)
async def get_test(
    test_result_id: UUID,
    test_result_service: TestResultService = Depends(get_test_result_service),
    current_user: UserData = Depends(require_permission("test_results.read"))
) -> TestResultDetailResponse:
    return await test_result_service.get_test_by_id(test_result_id)


@router.delete("/{test_result_id}", response_model=TestResultShortResponse)
async def delete_test(
    test_result_id: UUID,
    test_result_service: TestResultService = Depends(get_test_result_service),
    current_user: UserData = Depends(require_permission("test_results.delete"))
) -> TestResultShortResponse:
    return await test_result_service.delete_test(test_result_id)

# @router.post("/{test_result_id}/restore", response_model=TestDetailResponse)
# async def restore_test(
#     test_result_id: UUID,
#     test_result_service: TestService = Depends(get_test_result_service),
#     current_user: UserData = Depends(require_permission("test_results.restore"))
# ) -> TestDetailResponse:
#     return await test_result_service.restore_test(test_result_id)
