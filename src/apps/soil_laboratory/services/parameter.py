from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import Parameter
from apps.soil_laboratory.repositories.parameter import ParameterRepository
from apps.soil_laboratory.schemas.parameter import (
    ParameterDetailResponse,
    ParameterListItemResponse,
    ParameterPaginatedListResponse
)
from apps.soil_laboratory.specifications import (
    ParameterOrderingSpecification,
    ParameterSearchSpecification
)
from core.exceptions.database import EntityNotFoundError
from specifications.pagination import PaginationSpecification


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
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None
    ) -> ParameterPaginatedListResponse:
        search_spec = ParameterSearchSpecification(q)

        total_parameters = await self.parameter_repo.get_count_n(search_spec=search_spec)
        total_pages = max((total_parameters + page_size - 1) // page_size, 1)

        parameter_entities = await self.parameter_repo.get_all_paginated_n(
            PaginationSpecification(page_number, page_size),
            ParameterOrderingSpecification(ordering),
            search_spec=search_spec
        )
        response_items = [
            ParameterListItemResponse.model_validate(parameter)
            for parameter in parameter_entities
        ]

        return ParameterPaginatedListResponse(
            data=response_items,
            page=page_number,
            total_pages=total_pages,
            total_items=total_parameters
        )
