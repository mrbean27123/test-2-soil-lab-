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
    MaterialSearchSpecification
)
from core.exceptions.database import EntityNotFoundError
from specifications.pagination import PaginationSpecification


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
        filter_spec = MaterialFilterSpecification(material_type_code__eq=material_type_code__eq)
        search_spec = MaterialSearchSpecification(q)

        total_materials = await self.material_repo.get_count_n(filter_spec, search_spec)
        total_pages = max((total_materials + page_size - 1) // page_size, 1)

        material_entities = await self.material_repo.get_all_paginated_n(
            PaginationSpecification(page_number, page_size),
            MaterialOrderingSpecification(ordering),
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

    # async def get_material_lookup_options(
    #     self,
    #     limit: int = 100,
    #     offset: int = 0,
    #     search: str | None = None
    # ) -> list[MaterialLookupResponse]:
    #     material_entities = await self.material_repo.get_for_lookup(
    #         PaginationCriteria(limit, offset),
    #         where_conditions=[Material.archived_at == None, ],
    #         search=SearchCriteria(search, Material.name),
    #         order=OrderCriteria(Material.name),
    #     )
    #     response_items = [
    #         MaterialLookupResponse.model_validate(material)
    #         for material in material_entities
    #     ]
    #
    #     return response_items

    # async def get_materials_paginated(
    #     self,
    #     page: int,
    #     per_page: int
    # ) -> MaterialPaginatedListResponse:
    #     conditions = [Material.archived_at == None, ]
    #
    #     total_materials = await self.material_repo.get_count(where_conditions=conditions)
    #     total_pages = max((total_materials + per_page - 1) // per_page, 1)
    #     offset = (page - 1) * per_page
    #
    #     material_entities = await self.material_repo.get_all_paginated(
    #         PaginationCriteria(per_page, offset),
    #         where_conditions=conditions,
    #         order=OrderCriteria(Material.name),
    #         include=[MaterialLoadOptions.MATERIAL_TYPE, ]
    #     )
    #     response_items = [
    #         MaterialListItemResponse.model_validate(material)
    #         for material in material_entities
    #     ]
    #
    #     return MaterialPaginatedListResponse(
    #         data=response_items,
    #         page=page,
    #         total_pages=total_pages,
    #         total_items=total_materials
    #     )
