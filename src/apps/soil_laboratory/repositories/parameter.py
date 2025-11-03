from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, selectinload

from apps.soil_laboratory.models import Parameter
from repositories.base import (
    ArchiveByStatusMixin,
    BaseRepository,
    CreateMixin,
    ExistsMixin,
    ReadByIdMixin,
    ReadPaginatedMixin,
    UpdateMixin
)


class ParameterLoadOptions(str, Enum):
    SPECIFICATIONS = "specifications"
    TEST_RESULTS = "test_results"


class ParameterRepository(
    BaseRepository[Parameter, ParameterLoadOptions],
    ExistsMixin[Parameter],
    ReadPaginatedMixin[Parameter, ParameterLoadOptions],
    ReadByIdMixin[Parameter, ParameterLoadOptions],
    CreateMixin[Parameter],
    UpdateMixin[Parameter],
    ArchiveByStatusMixin[Parameter]
):
    _LOAD_OPTIONS_MAP: dict[ParameterLoadOptions, Load] = {
        ParameterLoadOptions.SPECIFICATIONS: selectinload(Parameter.specifications),
        ParameterLoadOptions.TEST_RESULTS: selectinload(Parameter.test_results)
    }

    def __init__(self, db: AsyncSession):
        super().__init__(db, Parameter)
