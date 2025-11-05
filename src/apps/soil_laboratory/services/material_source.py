from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import MaterialSource
from apps.soil_laboratory.repositories.material_source import MaterialSourceRepository
from apps.soil_laboratory.schemas.material_source import (
    MaterialSourceDetailResponse,
    MaterialSourceListItemResponse,
    MaterialSourcePaginatedListResponse
)
from apps.soil_laboratory.specifications import (
    MaterialSourceFilterSpecification,
    MaterialSourceOrderingSpecification,
    MaterialSourceSearchSpecification,
    PaginationSpecification
)
from core.exceptions.database import EntityNotFoundError


class MaterialSourceService:
    def __init__(self, db: AsyncSession, material_source_repo: MaterialSourceRepository):
        self.db = db
        self.material_source_repo = material_source_repo

    async def get_material_source_by_id(
        self,
        material_source_id: UUID
    ) -> MaterialSourceDetailResponse:
        material_source = await self.material_source_repo.get_by_id(material_source_id)

        if not material_source:
            raise EntityNotFoundError(MaterialSource, material_source_id)

        return MaterialSourceDetailResponse.model_validate(material_source)

    async def get_material_sources_paginated(
        self,
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None
    ) -> MaterialSourcePaginatedListResponse:
        pagination_spec = PaginationSpecification(page_number, page_size)
        ordering_spec = MaterialSourceOrderingSpecification(ordering)
        filter_spec = MaterialSourceFilterSpecification()
        search_spec = MaterialSourceSearchSpecification(q)

        total_material_sources = await self.material_source_repo.get_count(filter_spec, search_spec)
        total_pages = pagination_spec.get_total_pages(total_material_sources)

        material_source_entities = await self.material_source_repo.get_all_paginated(
            pagination_spec,
            ordering_spec,
            filter_spec,
            search_spec
        )
        response_items = [
            MaterialSourceListItemResponse.model_validate(material_source)
            for material_source in material_source_entities
        ]

        return MaterialSourcePaginatedListResponse(
            data=response_items,
            page=page_number,
            total_pages=total_pages,
            total_items=total_material_sources
        )
