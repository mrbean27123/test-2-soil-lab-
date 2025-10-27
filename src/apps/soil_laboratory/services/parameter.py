from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import Parameter
from apps.soil_laboratory.repositories.parameter import ParameterRepository
from apps.soil_laboratory.schemas.parameter import (
    ParameterDetailResponse,
    ParameterListItemResponse,
    ParameterPaginatedListResponse
)
from core.exceptions.database import EntityNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria


class ParameterService:
    def __init__(self, db: AsyncSession, parameter_repo: ParameterRepository):
        self.db = db
        self.parameter_repo = parameter_repo

    async def get_parameter_by_id(self, parameter_id: UUID) -> ParameterDetailResponse:
        parameter = await self.parameter_repo.get_by_id(parameter_id)

        if not parameter:
            raise EntityNotFoundError(Parameter, parameter_id)

        return ParameterDetailResponse.model_validate(parameter)

    async def get_parameters_paginated(
        self,
        page: int,
        per_page: int
    ) -> ParameterPaginatedListResponse:
        conditions = [Parameter.archived_at == None, ]

        total_materials = await self.parameter_repo.get_count(where_conditions=conditions)
        total_pages = max((total_materials + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        material_entities = await self.parameter_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=conditions,
            order=OrderCriteria(Parameter.name)
        )
        response_items = [
            ParameterListItemResponse.model_validate(material)
            for material in material_entities
        ]

        return ParameterPaginatedListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_materials
        )
