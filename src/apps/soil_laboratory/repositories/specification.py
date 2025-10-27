from enum import Enum

from sqlalchemy import BinaryExpression, BooleanClauseList, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Material, Specification
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


class SpecificationLoadOptions(str, Enum):
    PARAMETER = "parameter"
    MATERIAL = "material"
    MATERIAL__MATERIAL_TYPE = "material__material_type"
    MATERIAL_SOURCE = "material_source"


class SpecificationRepository(
    BaseRepository[Specification, SpecificationLoadOptions],
    ExistsMixin[Specification],
    CountMixin[Specification],
    LookupMixin[Specification],
    ReadPaginatedMixin[Specification, SpecificationLoadOptions],
    ReadByIdMixin[Specification, SpecificationLoadOptions],
    CreateMixin[Specification],
    UpdateMixin[Specification],
    ArchiveByStatusMixin[Specification]
):
    _LOAD_OPTIONS_MAP: dict[SpecificationLoadOptions, Load] = {
        SpecificationLoadOptions.PARAMETER: selectinload(Specification.parameter),
        SpecificationLoadOptions.MATERIAL: selectinload(Specification.material),
        SpecificationLoadOptions.MATERIAL__MATERIAL_TYPE: (
            selectinload(Specification.material).selectinload(Material.material_type)
        ),
        SpecificationLoadOptions.MATERIAL_SOURCE: selectinload(Specification.material_source)
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Specification)

    async def get_by_conditions(
        self,
        where_conditions: list[BinaryExpression | BooleanClauseList] | None = None,
        include: list[SpecificationLoadOptions] | None = None
    ) -> Specification | None:
        """Retrieve a single object of Specification by conditions."""
        stmt = select(Specification).where(and_(*where_conditions))
        stmt = self._apply_load_options(stmt, include)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
