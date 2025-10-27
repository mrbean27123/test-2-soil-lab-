from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login, require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_material_type_service
from apps.soil_laboratory.schemas.material_type import MaterialTypePaginatedListResponse
from apps.soil_laboratory.services.material_type import MaterialTypeService


router = APIRouter(prefix="/material-types", tags=["material-types"])


@router.get("/lookups", response_model=MaterialTypePaginatedListResponse)
async def get_material_type_lookups_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    material_type_service: MaterialTypeService = Depends(get_material_type_service),
    current_user: UserData = Depends(require_permission(require_login()))
) -> MaterialTypePaginatedListResponse:
    return await material_type_service.get_material_types_paginated(page, per_page)
