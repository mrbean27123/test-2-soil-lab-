from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.dto.test import TestCreateDTO
from apps.soil_laboratory.enums import TestStatus, TestType
from apps.soil_laboratory.models import Sample, Test
from apps.soil_laboratory.molding_sand_config import (
    GAS_PERMEABILITY_CONSTRAINTS,
    MOISTURE_CONSTRAINTS, MoldingSandRecipes,
    STRENGTH_CONSTRAINTS
)
from apps.soil_laboratory.repositories.sample import SampleLoadOptions, SampleRepository
from apps.soil_laboratory.repositories.test import TestLoadOptions, TestRepository
from apps.soil_laboratory.schemas.test import (
    TestCreate,
    TestDetailResponse,
    TestListItemResponse,
    TestListResponse,
    TestLookupResponse, TestShortResponse
)
from core.exceptions.database import EntityNotFoundError
from repositories.base import OrderCriteria, PaginationCriteria, SearchCriteria


class TestService:
    def __init__(self, db: AsyncSession, test_repo: TestRepository, sample_repo: SampleRepository):
        self.db = db
        self.test_repo = test_repo
        self.sample_repo = sample_repo

    async def get_test_by_id(self, test_id: UUID) -> TestDetailResponse:
        test = await self.test_repo.get_by_id(test_id, include=[TestLoadOptions.SAMPLE, ])

        if not test:
            raise EntityNotFoundError(Test, test_id)

        return TestDetailResponse.model_validate(test)

    async def get_test_lookup_options(
        self,
        limit: int = 100,
        offset: int = 0,
        search: str | None = None
    ) -> list[TestLookupResponse]:
        test_entities = await self.test_repo.get_for_lookup(
            PaginationCriteria(limit, offset),
            SearchCriteria(search, Test.mean_measurement),
            OrderCriteria(Test.created_at)
        )
        response_items = [
            TestLookupResponse.model_validate(test)
            for test in test_entities
        ]

        return response_items

    async def get_tests_paginated(self, page: int, per_page: int) -> TestListResponse:
        total_tests = await self.test_repo.get_count(
            where_conditions=[Test.deleted_at == None, ]
        )
        total_pages = max((total_tests + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        test_entities = await self.test_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=[Test.deleted_at == None, ],
            order=OrderCriteria(Test.created_at)
        )
        response_items = [
            TestListItemResponse.model_validate(test)
            for test in test_entities
        ]

        return TestListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_tests
        )

    async def create_test(
        self,
        test_data: TestCreate
    ) -> TestDetailResponse:
        sample = await self.sample_repo.get_by_id(
            test_data.sample_id,
            include=[SampleLoadOptions.TESTS, ]
        )

        if not sample:
            raise EntityNotFoundError(Sample, test_data.sample_id)

        test_dto = self._create_test_dto(sample, test_data)

        existing_test = None

        for test in sample.tests:
            if test.type_ == test_dto.type_:
                existing_test = test
                break

        if existing_test:
            await self.test_repo.hard_delete(existing_test.id)

        test = await self.test_repo.create(test_dto)

        await self.db.commit()

        return TestDetailResponse.model_validate(test)

    # async def update_test(
    #     self,
    #     test_id: UUID,
    #     test_data: TestUpdate
    # ) -> TestDetailResponse:
    #     test_data = self._validate_test_data(test_data)
    #     test = await self.test_repo.update(test_id, test_data.to_dto())
    #
    #     if not test:
    #         raise EntityNotFoundError(Test, test_id)
    #
    #     await self.db.commit()
    #
    #     await self.db.refresh(test)
    #
    #     return TestDetailResponse.model_validate(test)

    async def delete_test(self, test_id: UUID) -> TestShortResponse:
        deleted_test = await self.test_repo.hard_delete(test_id)

        if not deleted_test:
            raise EntityNotFoundError(Test, test_id)

        await self.db.commit()

        return TestShortResponse.model_validate(deleted_test)

    # async def restore_test(self, test_id: UUID) -> TestDetailResponse:
    #     restored_test = await self.test_repo.restore(test_id)
    #
    #     if not restored_test:
    #         raise EntityNotFoundError(Test, test_id)
    #
    #     await self.db.commit()
    #
    #     await self.db.refresh(restored_test)
    #
    #     return await self.get_test_by_id(restored_test.id)

    @staticmethod
    def _create_test_dto(
        sample: Sample,
        test_data: TestCreate,
    ) -> TestCreateDTO:
        if sample.molding_sand_recipe not in MoldingSandRecipes:
            raise ValueError(f"Unknown molding sand recipe: {sample.molding_sand_recipe}")

        test_type = test_data.type_
        measurement = test_data.measurement_1

        match test_type:
            case TestType.STRENGTH:
                constraints = STRENGTH_CONSTRAINTS
            case TestType.GAS_PERMEABILITY:
                constraints = GAS_PERMEABILITY_CONSTRAINTS
            case TestType.MOISTURE_PERCENT:
                constraints = MOISTURE_CONSTRAINTS

        lower_limit, upper_limit = constraints[sample.molding_sand_recipe]

        return TestCreateDTO(
            sample_id=sample.id,
            type_=test_type,
            measurement_1=measurement,
            measurement_2=measurement,

            selected_measurement_1=measurement,
            selected_measurement_2=measurement,

            difference_percent=0,
            mean_measurement=measurement,

            lower_limit=lower_limit,
            upper_limit=upper_limit,

            status=(
                TestStatus.PASSED
                if lower_limit <= measurement <= upper_limit
                else TestStatus.FAILED
            )
        )
