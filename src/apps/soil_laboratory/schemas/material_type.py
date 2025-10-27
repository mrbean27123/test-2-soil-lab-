from uuid import UUID

from pydantic import Field, field_validator

from apps.soil_laboratory.dto.material_type import MaterialTypeCreateDTO, MaterialTypeUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin


CODE_CONSTRAINTS = {"min_length": 1, "max_length": 255}
NAME_CONSTRAINTS = {"min_length": 1, "max_length": 255}


class MaterialTypeInputSchemaBase(InputSchemaBase):
    @field_validator("code", mode="after", check_fields=False)
    @classmethod
    def validate_code(cls, value: str) -> str:
        return value

    @field_validator("name", mode="after", check_fields=False)
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value


class MaterialTypeCreate(MaterialTypeInputSchemaBase):
    code: str = Field(**CODE_CONSTRAINTS)
    name: str = Field(**NAME_CONSTRAINTS)

    def to_dto(self) -> MaterialTypeCreateDTO:
        return MaterialTypeCreateDTO(**self.model_dump())


class MaterialTypeUpdate(MaterialTypeInputSchemaBase):
    code: str = Field(None, **CODE_CONSTRAINTS)
    name: str = Field(None, **NAME_CONSTRAINTS)

    def to_dto(self) -> MaterialTypeUpdateDTO:
        return MaterialTypeUpdateDTO(**self.model_dump(exclude_unset=True))


MaterialTypeResponseSchemaBase = ResponseSchemaBase[UUID]


class MaterialTypeLookupResponse(MaterialTypeResponseSchemaBase):
    code: str
    name: str


class MaterialTypeShortResponse(MaterialTypeResponseSchemaBase):
    code: str
    name: str


class MaterialTypeDetailResponse(
    MaterialTypeResponseSchemaBase,
    ReferenceEntitySchemaMetadataMixin
):
    code: str
    name: str
    # sample_types: list["SampleTypeShortResponse"]


class MaterialTypeListItemResponse(MaterialTypeShortResponse, ReferenceEntitySchemaMetadataMixin):
    pass


class MaterialTypePaginatedListResponse(PaginatedListResponseBase[MaterialTypeListItemResponse]):
    pass
