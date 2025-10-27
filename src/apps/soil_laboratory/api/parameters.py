from fastapi import APIRouter, Depends, Query

from apps.identity.dependencies.auth import require_login, require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_parameter_service
from apps.soil_laboratory.schemas.parameter import ParameterPaginatedListResponse
from apps.soil_laboratory.services.parameter import ParameterService


router = APIRouter(prefix="/parameters", tags=["parameters"])


@router.get("/lookups", response_model=ParameterPaginatedListResponse)
async def get_parameter_lookups_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    parameter_service: ParameterService = Depends(get_parameter_service),
    current_user: UserData = Depends(require_permission(require_login()))
) -> ParameterPaginatedListResponse:
    return await parameter_service.get_parameters_paginated(page, per_page)
