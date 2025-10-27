from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import Sample
from apps.soil_laboratory.repositories.sample import SampleLoadOptions, SampleRepository
from apps.soil_laboratory.schemas.sample import (
    SampleCreate,
    SampleDetailResponse,
    SampleListItemResponse,
    SamplePaginatedListResponse
)
from core.exceptions.database import EntityNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria


class SampleService:
    def __init__(self, db: AsyncSession, sample_repo: SampleRepository):
        self.db = db
        self.sample_repo = sample_repo

    async def get_sample_by_id(self, sample_id: UUID) -> SampleDetailResponse:
        sample = await self.sample_repo.get_by_id(
            sample_id,
            include=[
                SampleLoadOptions.MATERIAL__MATERIAL_TYPE,
                SampleLoadOptions.MATERIAL_SOURCE,
                SampleLoadOptions.TEST_RESULTS__PARAMETER
            ]
        )

        if not sample:
            raise EntityNotFoundError(Sample, sample_id)

        return SampleDetailResponse.model_validate(sample)

    # async def get_sample_lookup_options(
    #     self,
    #     limit: int = 100,
    #     offset: int = 0,
    #     search: str | None = None
    # ) -> list[SampleLookupResponse]:
    #     sample_entities = await self.sample_repo.get_for_lookup(
    #         PaginationCriteria(limit, offset),
    #         search=SearchCriteria(search, Sample.received_at),
    #         order=OrderCriteria(Sample.received_at)
    #     )
    #     response_items = [SampleLookupResponse.model_validate(sample) for sample in sample_entities]
    #
    #     return response_items

    async def get_samples_paginated(self, page: int, per_page: int) -> SamplePaginatedListResponse:
        conditions = [Sample.deleted_at == None, ]

        total_samples = await self.sample_repo.get_count(where_conditions=conditions)
        total_pages = max((total_samples + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        sample_entities = await self.sample_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=conditions,
            order=OrderCriteria(Sample.received_at),
            include=[
                SampleLoadOptions.MATERIAL__MATERIAL_TYPE,
                SampleLoadOptions.MATERIAL_SOURCE,
                SampleLoadOptions.TEST_RESULTS__PARAMETER
            ]
        )
        response_items = [
            SampleListItemResponse.model_validate(sample)
            for sample in sample_entities
        ]

        return SamplePaginatedListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_samples
        )

    async def create_sample(self, sample_data: SampleCreate) -> SampleDetailResponse:
        sample = await self.sample_repo.create(sample_data.to_dto())

        await self.db.commit()

        return await self.get_sample_by_id(sample.id)

    # async def update_sample(
    #     self,
    #     sample_id: UUID,
    #     sample_data: SampleUpdate
    # ) -> SampleDetailResponse:
    #     sample = await self.sample_repo.update(sample_id, sample_data.to_dto())
    #
    #     if not sample:
    #         raise EntityNotFoundError(Sample, sample_id)
    #
    #     await self.db.commit()
    #
    #     await self.db.refresh(sample)
    #
    #     return SampleDetailResponse.model_validate(sample)

    async def delete_sample(self, sample_id: UUID) -> SampleDetailResponse:
        deleted_sample = await self.sample_repo.soft_delete(sample_id)

        if not deleted_sample:
            raise EntityNotFoundError(Sample, sample_id)

        await self.db.commit()

        await self.db.refresh(deleted_sample)

        return await self.get_sample_by_id(deleted_sample.id)

    async def restore_sample(self, sample_id: UUID) -> SampleDetailResponse:
        restored_sample = await self.sample_repo.restore(sample_id)

        if not restored_sample:
            raise EntityNotFoundError(Sample, sample_id)

        await self.db.commit()

        await self.db.refresh(restored_sample)

        return await self.get_sample_by_id(restored_sample.id)
