from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import Parameter, Sample, Specification, TestResult
from apps.soil_laboratory.repositories import (
    MeasurementRepository,
    ParameterRepository,
    SampleLoadOptions,
    SampleRepository,
    SpecificationRepository
)
from apps.soil_laboratory.repositories.test_result import (
    TestResultLoadOptions,
    TestResultRepository
)
from apps.soil_laboratory.schemas.test_result import (
    TestResultCreate,
    TestResultDetailResponse,
    TestResultShortResponse
)
from apps.soil_laboratory.services.test_result.strategies import (
    resolve_strategies_and_get_test_result_create_dto
)
from core.exceptions.database import EntityNotFoundError


class TestResultService:
    def __init__(
        self,
        db: AsyncSession,
        test_result_repo: TestResultRepository,
        sample_repo: SampleRepository,
        parameter_repo: ParameterRepository,
        specification_repo: SpecificationRepository,
        measurement_repo: MeasurementRepository
    ):
        self.db = db
        self.test_result_repo = test_result_repo
        self.sample_repo = sample_repo
        self.parameter_repo = parameter_repo
        self.specification_repo = specification_repo
        self.measurement_repo = measurement_repo

    async def get_test_by_id(self, test_id: UUID) -> TestResultDetailResponse:
        test = await self.test_result_repo.get_by_id(
            test_id,
            include=[
                TestResultLoadOptions.SAMPLE__MATERIAL__MATERIAL_TYPE,
                TestResultLoadOptions.SAMPLE__MATERIAL_SOURCE,
                TestResultLoadOptions.PARAMETER,
                TestResultLoadOptions.MEASUREMENTS
            ]
        )

        if not test:
            raise EntityNotFoundError(TestResult, test_id)

        return TestResultDetailResponse.model_validate(test)

    async def create_test(self, test_result_data: TestResultCreate) -> TestResultDetailResponse:
        sample: Sample = await self.sample_repo.get_by_id(
            test_result_data.sample_id,
            include=[
                SampleLoadOptions.MATERIAL__MATERIAL_TYPE,
                SampleLoadOptions.MATERIAL_SOURCE,
                SampleLoadOptions.TEST_RESULTS__PARAMETER,
            ]
        )

        if not sample:
            raise EntityNotFoundError(Sample, test_result_data.sample_id)

        parameter = await self.parameter_repo.get_by_id(test_result_data.parameter_id)

        if not parameter:
            raise EntityNotFoundError(Parameter, test_result_data.parameter_id)

        specification = await self.specification_repo.get_by_conditions(
            where_conditions=[
                Specification.parameter_id == test_result_data.parameter_id,
                Specification.material_id == sample.material_id,
                Specification.material_source_id == sample.material_source_id
            ]
        )

        test_result_dto = resolve_strategies_and_get_test_result_create_dto(
            sample,
            parameter,
            test_result_data,
            specification
        )

        existing_test_result = None

        for test_result in sample.test_results:
            if test_result.parameter.id == test_result_dto.parameter_id:
                existing_test_result = test_result
                break

        if existing_test_result:
            await self.test_result_repo.hard_delete(existing_test_result.id)

        test_result = await self.test_result_repo.create(test_result_dto)

        await self.db.commit()

        return await self.get_test_by_id(test_result.id)

    # async def update_test(
    #     self,
    #     test_id: UUID,
    #     test_data: TestUpdate
    # ) -> TestDetailResponse:
    #     test_data = self._validate_test_data(test_data)
    #     test = await self.test_result_repo.update(test_id, test_data.to_dto())
    #
    #     if not test:
    #         raise EntityNotFoundError(Test, test_id)
    #
    #     await self.db.commit()
    #
    #     await self.db.refresh(test)
    #
    #     return TestDetailResponse.model_validate(test)

    async def delete_test(self, test_id: UUID) -> TestResultShortResponse:
        deleted_test = await self.test_result_repo.hard_delete(test_id)

        if not deleted_test:
            raise EntityNotFoundError(TestResult, test_id)

        await self.db.commit()

        return TestResultShortResponse.model_validate(deleted_test)
