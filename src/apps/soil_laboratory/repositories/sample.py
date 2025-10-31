from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Material, Sample, TestResult
from repositories.base import (
    BaseRepository,
    CreateMixin,
    ExistsMixin,
    HardDeleteMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    SoftDeleteMixin,
    UpdateMixin
)


class SampleLoadOptions(str, Enum):
    MATERIAL = "material"
    MATERIAL__MATERIAL_TYPE = "material__material_type"
    MATERIAL_SOURCE = "material_source"
    TEST_RESULTS = "test_results"
    TEST_RESULTS__PARAMETER = "test_results__parameter"


class SampleRepository(
    BaseRepository[Sample, SampleLoadOptions],
    ExistsMixin[Sample],
    ReadPaginatedMixin[Sample, SampleLoadOptions],
    ReadByIdMixin[Sample, SampleLoadOptions],
    CreateMixin[Sample],
    UpdateMixin[Sample],
    SoftDeleteMixin[Sample],
    HardDeleteMixin[Sample]
):
    _LOAD_OPTIONS_MAP: dict[SampleLoadOptions, Load] = {
        SampleLoadOptions.MATERIAL: selectinload(Sample.material),
        SampleLoadOptions.MATERIAL__MATERIAL_TYPE: (
            selectinload(Sample.material).selectinload(Material.material_type)
        ),
        SampleLoadOptions.MATERIAL_SOURCE: selectinload(Sample.material_source),
        SampleLoadOptions.TEST_RESULTS: selectinload(Sample.test_results),
        SampleLoadOptions.TEST_RESULTS__PARAMETER: (
            selectinload(Sample.test_results).selectinload(TestResult.parameter)
        ),
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Sample)
