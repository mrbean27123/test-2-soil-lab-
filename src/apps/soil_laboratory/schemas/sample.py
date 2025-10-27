from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field, field_validator

from apps.soil_laboratory.dto.sample import SampleCreateDTO, SampleUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase, SchemaBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.material import MaterialShortResponse
    from apps.soil_laboratory.schemas.material_source import MaterialSourceShortResponse
    from apps.soil_laboratory.schemas.test_result import TestResultShortResponse

NOTE_CONSTRAINTS = {"min_length": 1, "max_length": 1000}


class SampleInputSchemaBase(InputSchemaBase):
    @field_validator("note", mode="after", check_fields=False)
    @classmethod
    def validate_note(cls, value: str | None) -> str | None:
        return value


class SampleCreate(SampleInputSchemaBase):
    material_id: UUID
    material_source_id: UUID

    temperature: float
    received_at: datetime

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> SampleCreateDTO:
        return SampleCreateDTO(**self.model_dump())


class SampleUpdate(SampleInputSchemaBase):
    received_at: datetime = Field(None)

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> SampleUpdateDTO:
        return SampleUpdateDTO(**self.model_dump(exclude_unset=True))


SampleResponseBase = ResponseSchemaBase[UUID]


class SampleLookupResponse(SampleResponseBase):
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    received_at: datetime


class SampleShortResponse(SampleResponseBase):
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    received_at: datetime


class SampleDetailResponse(SampleResponseBase, BusinessEntitySchemaMetadataMixin):
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    temperature: float
    received_at: datetime

    test_results: list["TestResultShortResponse"]

    note: str | None


class SampleListItemResponse(SampleShortResponse, BusinessEntitySchemaMetadataMixin):
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    temperature: float
    received_at: datetime

    test_results: list["TestResultShortResponse"]


class SamplePaginatedListResponse(PaginatedListResponseBase[SampleListItemResponse]):
    pass


class SamplesReportGenerationRequest(SchemaBase):
    date_from: date | None = None
    date_to: date | None = None


class SamplesReportGenerationResponse(SchemaBase):
    success: bool
    message: str
    file_name: str
    total_records: int
    generated_at: datetime
