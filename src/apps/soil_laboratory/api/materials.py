from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_material_service
from apps.soil_laboratory.schemas.material import MaterialPaginatedListResponse
from apps.soil_laboratory.services.material import MaterialService


router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/lookups", response_model=MaterialPaginatedListResponse)
async def get_material_lookups_list(
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
    # Filters
    material_type_code__eq: str | None = Query(
        None,
        alias="filter[materialTypeCode][eq]",
        description="Material type code (string | comma-separated for multiple values)"
    ),
    # Dependencies
    material_service: MaterialService = Depends(get_material_service),
    current_user: UserData = Depends(require_login())
) -> MaterialPaginatedListResponse:
    return await material_service.get_materials_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q,
        material_type_code__eq=material_type_code__eq
    )
