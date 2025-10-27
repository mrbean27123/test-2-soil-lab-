from uuid import UUID

from pydantic import Field, field_validator

from apps.soil_laboratory.dto.parameter import ParameterCreateDTO, ParameterUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin


CODE_CONSTRAINTS = {"min_length": 1, "max_length": 255}
NAME_CONSTRAINTS = {"min_length": 1, "max_length": 255}
UNITS_CONSTRAINTS = {"min_length": 1, "max_length": 120}


class ParameterInputSchemaBase(InputSchemaBase):
    @field_validator("code", mode="after", check_fields=False)
    @classmethod
    def validate_code(cls, value: str) -> str:
        return value

    @field_validator("name", mode="after", check_fields=False)
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value

    @field_validator("units", mode="after", check_fields=False)
    @classmethod
    def validate_units(cls, value: str) -> str:
        return value


class ParameterCreate(ParameterInputSchemaBase):
    code: str = Field(**CODE_CONSTRAINTS)
    name: str = Field(**NAME_CONSTRAINTS)
    units: str | None = Field(**UNITS_CONSTRAINTS)

    def to_dto(self) -> ParameterCreateDTO:
        return ParameterCreateDTO(**self.model_dump())


class ParameterUpdate(ParameterInputSchemaBase):
    code: str = Field(None, **CODE_CONSTRAINTS)
    name: str = Field(None, **NAME_CONSTRAINTS)
    units: str | None = Field(None, **UNITS_CONSTRAINTS)

    def to_dto(self) -> ParameterUpdateDTO:
        return ParameterUpdateDTO(**self.model_dump(exclude_unset=True))


ParameterResponseSchemaBase = ResponseSchemaBase[UUID]


class ParameterLookupResponse(ParameterResponseSchemaBase):
    code: str
    name: str
    units: str | None = None


class ParameterShortResponse(ParameterResponseSchemaBase):
    code: str
    name: str
    units: str | None = None


class ParameterDetailResponse(ParameterResponseSchemaBase, ReferenceEntitySchemaMetadataMixin):
    code: str
    name: str
    units: str | None = None


class ParameterListItemResponse(ParameterShortResponse, ReferenceEntitySchemaMetadataMixin):
    pass


class ParameterPaginatedListResponse(PaginatedListResponseBase[ParameterListItemResponse]):
    pass
