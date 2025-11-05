from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_material_source_service
from apps.soil_laboratory.schemas.material_source import MaterialSourcePaginatedListResponse
from apps.soil_laboratory.services.material_source import MaterialSourceService


router = APIRouter(prefix="/material-sources", tags=["material-sources"])


@router.get("/lookups", response_model=MaterialSourcePaginatedListResponse)
async def get_material_source_lookups_list(
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
    material_source_service: MaterialSourceService = Depends(get_material_source_service),
    current_user: UserData = Depends(require_login())
) -> MaterialSourcePaginatedListResponse:
    return await material_source_service.get_material_sources_paginated(
        page_number=page_number,
        page_size=page_size,
        ordering=ordering,
        q=q
    )
