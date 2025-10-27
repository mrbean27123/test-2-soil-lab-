from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Material, Sample, TestResult
from repositories.base import (
    BaseRepository,
    CountMixin,
    CreateMixin,
    ExistsMixin,
    HardDeleteMixin,
    LookupMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    SoftDeleteMixin,
    UpdateMixin
)


class TestResultLoadOptions(str, Enum):
    SAMPLE = "sample"
    SAMPLE__MATERIAL__MATERIAL_TYPE = "sample__material__material_type"
    SAMPLE__MATERIAL_SOURCE = "sample__material_source"
    PARAMETER = "parameter"
    MEASUREMENTS = "measurements"


class TestResultRepository(
    BaseRepository[TestResult, TestResultLoadOptions],
    ExistsMixin[TestResult],
    CountMixin[TestResult],
    LookupMixin[TestResult],
    ReadPaginatedMixin[TestResult, TestResultLoadOptions],
    ReadByIdMixin[TestResult, TestResultLoadOptions],
    CreateMixin[TestResult],
    UpdateMixin[TestResult],
    SoftDeleteMixin[TestResult],
    HardDeleteMixin[TestResult]
):
    _LOAD_OPTIONS_MAP: dict[TestResultLoadOptions, Load] = {
        TestResultLoadOptions.SAMPLE: selectinload(TestResult.sample),
        TestResultLoadOptions.SAMPLE__MATERIAL__MATERIAL_TYPE: (
            selectinload(TestResult.sample)
            .selectinload(Sample.material)
            .selectinload(Material.material_type)
        ),
        TestResultLoadOptions.SAMPLE__MATERIAL_SOURCE: (
            selectinload(TestResult.sample).selectinload(Sample.material_source)
        ),
        TestResultLoadOptions.PARAMETER: selectinload(TestResult.parameter),
        TestResultLoadOptions.MEASUREMENTS: selectinload(TestResult.measurements)
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, TestResult)
