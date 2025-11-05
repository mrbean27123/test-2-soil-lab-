from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import MaterialType
from apps.soil_laboratory.repositories.material_type import MaterialTypeRepository
from apps.soil_laboratory.schemas.material_type import (
    MaterialTypeDetailResponse,
    MaterialTypeListItemResponse,
    MaterialTypePaginatedListResponse
)
from apps.soil_laboratory.specifications import (
    MaterialTypeFilterSpecification,
    MaterialTypeOrderingSpecification,
    MaterialTypeSearchSpecification,
    PaginationSpecification
)
from core.exceptions.database import EntityNotFoundError


class MaterialTypeService:
    def __init__(self, db: AsyncSession, material_type_repo: MaterialTypeRepository):
        self.db = db
        self.material_type_repo = material_type_repo

    async def get_material_type_by_id(self, material_type_id: UUID) -> MaterialTypeDetailResponse:
        material_type = await self.material_type_repo.get_by_id(material_type_id)

        if not material_type:
            raise EntityNotFoundError(MaterialType, material_type_id)

        return MaterialTypeDetailResponse.model_validate(material_type)

    async def get_material_types_paginated(
        self,
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None
    ) -> MaterialTypePaginatedListResponse:
        pagination_spec = PaginationSpecification(page_number, page_size)
        ordering_spec = MaterialTypeOrderingSpecification(ordering)
        filter_spec = MaterialTypeFilterSpecification()
        search_spec = MaterialTypeSearchSpecification(q)

        total_material_types = await self.material_type_repo.get_count(filter_spec, search_spec)
        total_pages = pagination_spec.get_total_pages(total_material_types)

        material_type_entities = await self.material_type_repo.get_all_paginated(
            pagination_spec,
            ordering_spec,
            filter_spec,
            search_spec
        )
        response_items = [
            MaterialTypeListItemResponse.model_validate(material_type)
            for material_type in material_type_entities
        ]

        return MaterialTypePaginatedListResponse(
            data=response_items,
            page=page_number,
            total_pages=total_pages,
            total_items=total_material_types
        )
