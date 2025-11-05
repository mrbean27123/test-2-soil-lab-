from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Measurement
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


class MeasurementLoadOptions(str, Enum):
    TEST_RESULT = "test_result"


class MeasurementRepository(
    BaseRepository[Measurement, MeasurementLoadOptions],
    ExistsMixin[Measurement],
    ReadPaginatedMixin[Measurement, MeasurementLoadOptions],
    ReadByIdMixin[Measurement, MeasurementLoadOptions],
    CreateMixin[Measurement],
    UpdateMixin[Measurement],
    SoftDeleteMixin[Measurement],
    HardDeleteMixin[Measurement]
):
    _LOAD_OPTIONS_MAP: dict[MeasurementLoadOptions, Load] = {
        MeasurementLoadOptions.TEST_RESULT: selectinload(Measurement.test_result),
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Measurement)
