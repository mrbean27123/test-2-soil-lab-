from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict, Field, field_validator

from apps.soil_laboratory.dto.sample import SampleCreateDTO, SampleUpdateDTO
from schemas.base import SchemaBase, InputSchemaBase, PaginatedListResponseBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin
from validation.common import validate_description


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.test import TestShortResponse

MOLDING_SAND_RECIPE_CONSTRAINTS = {"min_length": 1, "max_length": 50}
NOTE_CONSTRAINTS = {"min_length": 1, "max_length": 1000}


class SampleInputSchemaBase(InputSchemaBase):
    @field_validator("molding_sand_recipe", mode="after", check_fields=False)
    @classmethod
    def validate_molding_sand_recipe(cls, value: str) -> str:
        return value

    @field_validator("note", mode="after", check_fields=False)
    @classmethod
    def validate_note(cls, value: str | None) -> str | None:
        return (
            validate_description(value, only_ukrainian_letters=False)
            if value is not None else value
        )


class SampleCreate(SampleInputSchemaBase):
    molding_sand_recipe: str = Field(..., **MOLDING_SAND_RECIPE_CONSTRAINTS)
    received_at: datetime

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> SampleCreateDTO:
        return SampleCreateDTO(**self.model_dump())


class SampleUpdate(SampleInputSchemaBase):
    molding_sand_recipe: str = Field(None, **MOLDING_SAND_RECIPE_CONSTRAINTS)
    received_at: datetime = Field(None)

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> SampleUpdateDTO:
        return SampleUpdateDTO(**self.model_dump(exclude_unset=True))


class SampleResponseBase(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class SampleLookupResponse(SampleResponseBase):
    molding_sand_recipe: str
    received_at: datetime


class SampleShortResponse(SampleResponseBase):
    molding_sand_recipe: str
    received_at: datetime


class SampleDetailResponse(SampleResponseBase, BusinessEntitySchemaMetadataMixin):
    molding_sand_recipe: str
    received_at: datetime

    tests: list["TestShortResponse"]

    note: str | None


class SampleListItemResponse(SampleShortResponse, BusinessEntitySchemaMetadataMixin):
    molding_sand_recipe: str
    received_at: datetime

    tests: list["TestShortResponse"]


class SampleListResponse(PaginatedListResponseBase[SampleListItemResponse]):
    pass


class SamplesReportGenerationRequest(SchemaBase):
    date_from: date | None = None
    date_to: date | None = None


class SamplesReportGenerationResponse(SchemaBase):
    model_config = ConfigDict(populate_by_name=True)

    success: bool
    message: str
    file_name: str
    total_records: int
    generated_at: datetime
