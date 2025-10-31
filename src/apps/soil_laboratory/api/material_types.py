from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login, require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_material_type_service
from apps.soil_laboratory.schemas.material_type import MaterialTypePaginatedListResponse
from apps.soil_laboratory.services.material_type import MaterialTypeService


router = APIRouter(prefix="/material-types", tags=["material-types"])


@router.get("/lookups", response_model=MaterialTypePaginatedListResponse)
async def get_material_type_lookups_list(
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
    material_type_service: MaterialTypeService = Depends(get_material_type_service),
    current_user: UserData = Depends(require_permission(require_login()))
) -> MaterialTypePaginatedListResponse:
    return await material_type_service.get_material_types_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )
