from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login, require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_material_service
from apps.soil_laboratory.schemas.material import MaterialPaginatedListResponse
from apps.soil_laboratory.services.material import MaterialService


router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/lookups", response_model=MaterialPaginatedListResponse)
async def get_material_lookups_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    material_service: MaterialService = Depends(get_material_service),
    current_user: UserData = Depends(require_permission(require_login()))
) -> MaterialPaginatedListResponse:
    return await material_service.get_materials_paginated(page, per_page)
