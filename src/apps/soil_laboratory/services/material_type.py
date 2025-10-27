from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import MaterialType
from apps.soil_laboratory.repositories.material_type import MaterialTypeRepository
from apps.soil_laboratory.schemas.material_type import (
    MaterialTypeDetailResponse,
    MaterialTypeListItemResponse,
    MaterialTypePaginatedListResponse
)
from core.exceptions.database import EntityNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria


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
        page: int,
        per_page: int
    ) -> MaterialTypePaginatedListResponse:
        conditions = [MaterialType.archived_at == None, ]

        total_materials = await self.material_type_repo.get_count(where_conditions=conditions)
        total_pages = max((total_materials + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        material_entities = await self.material_type_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=conditions,
            order=OrderCriteria(MaterialType.name)
        )
        response_items = [
            MaterialTypeListItemResponse.model_validate(material)
            for material in material_entities
        ]

        return MaterialTypePaginatedListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_materials
        )
