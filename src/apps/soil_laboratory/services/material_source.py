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
    MaterialSourceOrderingSpecification,
    MaterialSourceSearchSpecification
)
from core.exceptions.database import EntityNotFoundError
from specifications.pagination import PaginationSpecification


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
        search_spec = MaterialSourceSearchSpecification(q)

        total_material_sources = await self.material_source_repo.get_count_n(
            search_spec=search_spec
        )
        total_pages = max((total_material_sources + page_size - 1) // page_size, 1)

        material_source_entities = await self.material_source_repo.get_all_paginated_n(
            PaginationSpecification(page_number, page_size),
            MaterialSourceOrderingSpecification(ordering),
            search_spec=search_spec
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
