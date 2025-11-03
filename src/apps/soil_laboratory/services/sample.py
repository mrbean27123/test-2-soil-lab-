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
from apps.soil_laboratory.specifications import (
    SampleFilterSpecification,
    SampleOrderingSpecification,
    SampleSearchSpecification
)
from core.exceptions.database import EntityNotFoundError
from specifications.pagination import PaginationSpecification


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

    async def get_samples_paginated(
        self,
        page_number: int,
        page_size: int,
        ordering: str | None = None,
        q: str | None = None,
        material_type_id__eq: str | None = None,
        material_type_code__eq: str | None = None,
        material_id__eq: str | None = None,
        material_source_id__eq: str | None = None,
        material_source_code__eq: str | None = None
    ) -> SamplePaginatedListResponse:
        filter_spec = SampleFilterSpecification(
            material_type_id__eq=material_type_id__eq,
            material_type_code__eq=material_type_code__eq,
            material_id__eq=material_id__eq,
            material_source_id__eq=material_source_id__eq,
            material_source_code__eq=material_source_code__eq
        )
        search_spec = SampleSearchSpecification(q)

        total_samples = await self.sample_repo.get_count_n(filter_spec, search_spec)
        total_pages = max((total_samples + page_size - 1) // page_size, 1)

        sample_entities = await self.sample_repo.get_all_paginated_n(
            PaginationSpecification(page_number, page_size),
            SampleOrderingSpecification(ordering),
            filter_spec,
            search_spec,
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
            page=page_number,
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
