from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load

from apps.soil_laboratory.models import Measurement
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


class MeasurementLoadOptions(str, Enum):
    pass


class MeasurementRepository(
    BaseRepository[Measurement, MeasurementLoadOptions],
    ExistsMixin[Measurement],
    CountMixin[Measurement],
    LookupMixin[Measurement],
    ReadPaginatedMixin[Measurement, MeasurementLoadOptions],
    ReadByIdMixin[Measurement, MeasurementLoadOptions],
    CreateMixin[Measurement],
    UpdateMixin[Measurement],
    SoftDeleteMixin[Measurement]
):
    _LOAD_OPTIONS_MAP: dict[MeasurementLoadOptions, Load] = {}

    def __init__(self, db: AsyncSession):
        super().__init__(db, Measurement)
