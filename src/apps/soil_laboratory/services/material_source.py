from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import MaterialSource
from apps.soil_laboratory.repositories.material_source import (
    MaterialSourceRepository
)
from apps.soil_laboratory.schemas.material_source import (
    MaterialSourceDetailResponse,
    MaterialSourceListItemResponse,
    MaterialSourcePaginatedListResponse
)
from core.exceptions.database import EntityNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria


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
        page: int,
        per_page: int
    ) -> MaterialSourcePaginatedListResponse:
        conditions = [MaterialSource.archived_at == None, ]

        total_materials = await self.material_source_repo.get_count(where_conditions=conditions)
        total_pages = max((total_materials + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        material_entities = await self.material_source_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=conditions,
            order=OrderCriteria(MaterialSource.name)
        )
        response_items = [
            MaterialSourceListItemResponse.model_validate(material)
            for material in material_entities
        ]

        return MaterialSourcePaginatedListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_materials
        )
