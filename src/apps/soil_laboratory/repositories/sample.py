from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Sample
from repositories.base import (
    BaseRepository,
    CountMixin,
    CreateMixin,
    ExistsMixin,
    LookupMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    SoftDeleteMixin,
    UpdateMixin
)


class SampleLoadOptions(str, Enum):
    TESTS = "tests"


class SampleRepository(
    BaseRepository[Sample, SampleLoadOptions],
    ExistsMixin[Sample],
    CountMixin[Sample],
    LookupMixin[Sample],
    ReadPaginatedMixin[Sample, SampleLoadOptions],
    ReadByIdMixin[Sample, SampleLoadOptions],
    CreateMixin[Sample],
    UpdateMixin[Sample],
    SoftDeleteMixin[Sample]
):
    _LOAD_OPTIONS_MAP: dict[SampleLoadOptions, Load] = {
        SampleLoadOptions.TESTS: selectinload(Sample.tests),
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Sample)
