from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.soil_laboratory.dto.sample import SampleCreateDTO, SampleUpdateDTO
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin
from validation.common import validate_description


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.test import TestShortResponse

MOLDING_SAND_RECIPE_CONSTRAINTS = {"min_length": 1, "max_length": 50}
NOTE_CONSTRAINTS = {"min_length": 1, "max_length": 1000}


class SampleInputBase(InputBase):
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


class SampleCreate(SampleInputBase):
    molding_sand_recipe: str = Field(
        ...,
        **MOLDING_SAND_RECIPE_CONSTRAINTS,
        alias="moldingSandRecipe"
    )
    received_at: datetime = Field(..., alias="receivedAt")

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> SampleCreateDTO:
        return SampleCreateDTO(**self.model_dump())


class SampleUpdate(SampleInputBase):
    molding_sand_recipe: str = Field(
        None,
        **MOLDING_SAND_RECIPE_CONSTRAINTS,
        alias="moldingSandRecipe"
    )
    received_at: datetime = Field(None, alias="receivedAt")

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> SampleUpdateDTO:
        return SampleUpdateDTO(**self.model_dump(exclude_unset=True))


class SampleResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID


class SampleLookupResponse(SampleResponseBase):
    molding_sand_recipe: str = Field(alias="moldingSandRecipe")
    received_at: datetime = Field(alias="receivedAt")


class SampleShortResponse(SampleResponseBase):
    molding_sand_recipe: str = Field(alias="moldingSandRecipe")
    received_at: datetime = Field(alias="receivedAt")


class SampleDetailResponse(SampleResponseBase, BusinessEntitySchemaMetadataMixin):
    molding_sand_recipe: str = Field(alias="moldingSandRecipe")
    received_at: datetime = Field(alias="receivedAt")

    tests: list["TestShortResponse"]

    note: str | None


class SampleListItemResponse(SampleShortResponse, BusinessEntitySchemaMetadataMixin):
    molding_sand_recipe: str = Field(alias="moldingSandRecipe")
    received_at: datetime = Field(alias="receivedAt")

    tests: list["TestShortResponse"]


class SampleListResponse(PaginatedListResponseBase[SampleListItemResponse]):
    pass


class SamplesReportGenerationRequest(BaseModel):
    date_from: date | None = Field(alias="dateFrom")
    date_to: date | None = Field(alias="dateTo")


class SamplesReportGenerationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    success: bool
    message: str
    file_name: str = Field(alias="fileName")
    total_records: int = Field(alias="totalRecords")
    generated_at: datetime = Field(alias="generatedAt")
