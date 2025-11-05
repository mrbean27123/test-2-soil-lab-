from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_parameter_service
from apps.soil_laboratory.schemas.parameter import ParameterPaginatedListResponse
from apps.soil_laboratory.services.parameter import ParameterService


router = APIRouter(prefix="/parameters", tags=["parameters"])


@router.get("/lookups", response_model=ParameterPaginatedListResponse)
async def get_parameter_lookups_list(
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
    parameter_service: ParameterService = Depends(get_parameter_service),
    current_user: UserData = Depends(require_login())
) -> ParameterPaginatedListResponse:
    return await parameter_service.get_parameters_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )
