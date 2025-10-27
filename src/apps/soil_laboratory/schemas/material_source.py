from uuid import UUID

from pydantic import Field, field_validator

from apps.soil_laboratory.dto.material_source import (
    MaterialSourceCreateDTO,
    MaterialSourceUpdateDTO
)
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin


CODE_CONSTRAINTS = {"min_length": 1, "max_length": 255}
NAME_CONSTRAINTS = {"min_length": 1, "max_length": 255}


class MaterialSourceInputSchemaBase(InputSchemaBase):
    @field_validator("code", mode="after", check_fields=False)
    @classmethod
    def validate_code(cls, value: str) -> str:
        return value

    @field_validator("name", mode="after", check_fields=False)
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value


class MaterialSourceCreate(MaterialSourceInputSchemaBase):
    code: str = Field(**CODE_CONSTRAINTS)
    name: str = Field(**NAME_CONSTRAINTS)

    def to_dto(self) -> MaterialSourceCreateDTO:
        return MaterialSourceCreateDTO(**self.model_dump())


class MaterialSourceUpdate(MaterialSourceInputSchemaBase):
    code: str = Field(None, **CODE_CONSTRAINTS)
    name: str = Field(None, **NAME_CONSTRAINTS)

    def to_dto(self) -> MaterialSourceUpdateDTO:
        return MaterialSourceUpdateDTO(**self.model_dump(exclude_unset=True))


MaterialSourceResponseSchemaBase = ResponseSchemaBase[UUID]


class MaterialSourceLookupResponse(MaterialSourceResponseSchemaBase):
    code: str
    name: str


class MaterialSourceShortResponse(MaterialSourceResponseSchemaBase):
    code: str
    name: str


class MaterialSourceDetailResponse(
    MaterialSourceResponseSchemaBase,
    ReferenceEntitySchemaMetadataMixin
):
    code: str
    name: str


class MaterialSourceListItemResponse(
    MaterialSourceShortResponse,
    ReferenceEntitySchemaMetadataMixin
):
    pass


class MaterialSourcePaginatedListResponse(
    PaginatedListResponseBase[MaterialSourceListItemResponse]
):
    pass
