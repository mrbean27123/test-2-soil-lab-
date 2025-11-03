from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import MaterialType
from repositories.base import (
    ArchiveByStatusMixin,
    BaseRepository,
    CreateMixin,
    ExistsMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    UpdateMixin
)


class MaterialTypeLoadOptions(str, Enum):
    MATERIALS = "materials"


class MaterialTypeRepository(
    BaseRepository[MaterialType, MaterialTypeLoadOptions],
    ExistsMixin[MaterialType],
    ReadPaginatedMixin[MaterialType, MaterialTypeLoadOptions],
    ReadByIdMixin[MaterialType, MaterialTypeLoadOptions],
    CreateMixin[MaterialType],
    UpdateMixin[MaterialType],
    ArchiveByStatusMixin[MaterialType]
):
    _LOAD_OPTIONS_MAP: dict[MaterialTypeLoadOptions, Load] = {
        MaterialTypeLoadOptions.MATERIALS: selectinload(MaterialType.materials),
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, MaterialType)
