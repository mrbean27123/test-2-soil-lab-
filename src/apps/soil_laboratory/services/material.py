from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import Material
from apps.soil_laboratory.repositories.material import MaterialLoadOptions, MaterialRepository
from apps.soil_laboratory.schemas.material import (
    MaterialDetailResponse,
    MaterialListItemResponse,
    MaterialPaginatedListResponse
)
from apps.soil_laboratory.specifications import (
    MaterialFilterSpecification,
    MaterialOrderingSpecification,
    MaterialSearchSpecification,
    PaginationSpecification
)
from core.exceptions.database import EntityNotFoundError


class MaterialService:
    def __init__(self, db: AsyncSession, material_repo: MaterialRepository):
        self.db = db
        self.material_repo = material_repo

    async def get_material_by_id(self, material_id: UUID) -> MaterialDetailResponse:
        material = await self.material_repo.get_by_id(
            material_id,
            include=[MaterialLoadOptions.MATERIAL_TYPE, ]
        )

        if not material:
            raise EntityNotFoundError(Material, material_id)

        return MaterialDetailResponse.model_validate(material)

    async def get_materials_paginated(
        self,
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None,
        material_type_code__eq: str | None = None
    ) -> MaterialPaginatedListResponse:
        pagination_spec = PaginationSpecification(page_number, page_size)
        ordering_spec = MaterialOrderingSpecification(ordering)
        filter_spec = MaterialFilterSpecification(material_type_code__eq=material_type_code__eq)
        search_spec = MaterialSearchSpecification(q)

        total_materials = await self.material_repo.get_count(filter_spec, search_spec)
        total_pages = pagination_spec.get_total_pages(total_materials)

        material_entities = await self.material_repo.get_all_paginated(
            pagination_spec,
            ordering_spec,
            filter_spec,
            search_spec,
            include=[MaterialLoadOptions.MATERIAL_TYPE, ]
        )
        response_items = [
            MaterialListItemResponse.model_validate(material)
            for material in material_entities
        ]

        return MaterialPaginatedListResponse(
            data=response_items,
            page=page_number,
            total_pages=total_pages,
            total_items=total_materials
        )
