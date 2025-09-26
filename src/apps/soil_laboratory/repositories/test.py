from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Test
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


class TestLoadOptions(str, Enum):
    SAMPLE = "sample"


class TestRepository(
    BaseRepository[Test, TestLoadOptions],
    ExistsMixin[Test],
    CountMixin[Test],
    LookupMixin[Test],
    ReadPaginatedMixin[Test, TestLoadOptions],
    ReadByIdMixin[Test, TestLoadOptions],
    CreateMixin[Test],
    UpdateMixin[Test],
    SoftDeleteMixin[Test],
    HardDeleteMixin[Test],
):
    _LOAD_OPTIONS_MAP: dict[TestLoadOptions, Load] = {
        TestLoadOptions.SAMPLE: selectinload(Test.sample),
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Test)
