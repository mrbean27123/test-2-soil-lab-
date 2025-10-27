from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from apps.soil_laboratory.dto.measurement import MeasurementCreateDTO, MeasurementUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.test_result import TestResultShortResponse


class MeasurementInputSchemaBase(InputSchemaBase):
    pass


class MeasurementCreate(MeasurementInputSchemaBase):
    test_result_id: UUID
    value: float

    def to_dto(self) -> MeasurementCreateDTO:
        return MeasurementCreateDTO(**self.model_dump())


class MeasurementUpdate(MeasurementInputSchemaBase):
    value: float = Field(None)

    def to_dto(self) -> MeasurementUpdateDTO:
        return MeasurementUpdateDTO(**self.model_dump(exclude_unset=True))


MeasurementResponseSchemaBase = ResponseSchemaBase[UUID]


class MeasurementLookupResponse(MeasurementResponseSchemaBase):
    value: float


class MeasurementShortResponse(MeasurementResponseSchemaBase):
    value: float


class MeasurementDetailResponse(MeasurementResponseSchemaBase, BusinessEntitySchemaMetadataMixin):
    test_result: "TestResultShortResponse"
    value: float


class MeasurementListItemResponse(MeasurementResponseSchemaBase, BusinessEntitySchemaMetadataMixin):
    test_result: "TestResultShortResponse"
    value: float


class MeasurementPaginatedListResponse(PaginatedListResponseBase[MeasurementListItemResponse]):
    pass
