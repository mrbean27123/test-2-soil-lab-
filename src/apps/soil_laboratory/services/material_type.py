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
    MaterialTypeOrderingSpecification,
    MaterialTypeSearchSpecification
)
from core.exceptions.database import EntityNotFoundError
from specifications.pagination import PaginationSpecification


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
        search_spec = MaterialTypeSearchSpecification(q)

        total_material_types = await self.material_type_repo.get_count_n(search_spec=search_spec)
        total_pages = max((total_material_types + page_size - 1) // page_size, 1)

        material_type_entities = await self.material_type_repo.get_all_paginated_n(
            PaginationSpecification(page_number, page_size),
            MaterialTypeOrderingSpecification(ordering),
            search_spec=search_spec
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
