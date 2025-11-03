from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import MaterialSource
from repositories.base import (
    ArchiveByStatusMixin,
    BaseRepository,
    CreateMixin,
    ExistsMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    UpdateMixin
)


class MaterialSourceLoadOptions(str, Enum):
    SAMPLES = "samples"
    SPECIFICATIONS = "specifications"


class MaterialSourceRepository(
    BaseRepository[MaterialSource, MaterialSourceLoadOptions],
    ExistsMixin[MaterialSource],
    ReadPaginatedMixin[MaterialSource, MaterialSourceLoadOptions],
    ReadByIdMixin[MaterialSource, MaterialSourceLoadOptions],
    CreateMixin[MaterialSource],
    UpdateMixin[MaterialSource],
    ArchiveByStatusMixin[MaterialSource]
):
    _LOAD_OPTIONS_MAP: dict[MaterialSourceLoadOptions, Load] = {
        MaterialSourceLoadOptions.SAMPLES: selectinload(MaterialSource.samples),
        MaterialSourceLoadOptions.SPECIFICATIONS: selectinload(MaterialSource.specifications)
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, MaterialSource)
