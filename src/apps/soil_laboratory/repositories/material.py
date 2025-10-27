from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Material
from repositories.base import (
    ArchiveByStatusMixin,
    BaseRepository,
    CountMixin,
    CreateMixin,
    ExistsMixin,
    LookupMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    UpdateMixin
)


class MaterialLoadOptions(str, Enum):
    MATERIAL_TYPE = "material_type"


class MaterialRepository(
    BaseRepository[Material, MaterialLoadOptions],
    ExistsMixin[Material],
    CountMixin[Material],
    LookupMixin[Material],
    ReadPaginatedMixin[Material, MaterialLoadOptions],
    ReadByIdMixin[Material, MaterialLoadOptions],
    CreateMixin[Material],
    UpdateMixin[Material],
    ArchiveByStatusMixin[Material]
):
    _LOAD_OPTIONS_MAP: dict[MaterialLoadOptions, Load] = {
        MaterialLoadOptions.MATERIAL_TYPE: selectinload(Material.material_type),
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Material)
