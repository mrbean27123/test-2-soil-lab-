from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login, require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_material_source_service
from apps.soil_laboratory.schemas.material_source import MaterialSourcePaginatedListResponse
from apps.soil_laboratory.services.material_source import MaterialSourceService


router = APIRouter(prefix="/material-sources", tags=["material-sources"])


@router.get("/lookups", response_model=MaterialSourcePaginatedListResponse)
async def get_material_source_lookups_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    material_source_service: MaterialSourceService = Depends(get_material_source_service),
    current_user: UserData = Depends(require_permission(require_login()))
) -> MaterialSourcePaginatedListResponse:
    return await material_source_service.get_material_sources_paginated(page, per_page)
