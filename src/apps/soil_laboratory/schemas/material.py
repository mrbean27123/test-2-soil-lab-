from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field, field_validator

from apps.soil_laboratory.dto.material import MaterialCreateDTO, MaterialUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.material_type import MaterialTypeShortResponse

NAME_CONSTRAINTS = {"min_length": 1, "max_length": 120}


class MaterialInputSchemaBase(InputSchemaBase):
    @field_validator("name", mode="after", check_fields=False)
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        return value


class MaterialCreate(MaterialInputSchemaBase):
    material_type_id: UUID

    name: str = Field(**NAME_CONSTRAINTS)

    def to_dto(self) -> MaterialCreateDTO:
        return MaterialCreateDTO(**self.model_dump())


class MaterialUpdate(MaterialInputSchemaBase):
    material_type_id: UUID = Field(None)

    name: str = Field(None, **NAME_CONSTRAINTS)

    def to_dto(self) -> MaterialUpdateDTO:
        return MaterialUpdateDTO(**self.model_dump(exclude_unset=True))


MaterialResponseBase = ResponseSchemaBase[UUID]


class MaterialLookupResponse(MaterialResponseBase):
    material_type: "MaterialTypeShortResponse"
    name: str

    # @model_validator(mode="before")
    # @classmethod
    # def check_card_number_not_present(cls, data: Any) -> Any:
    #     from apps.soil_laboratory.models.material import Material
    #
    #     if isinstance(data, Material):
    #         obj = copy.copy(data)
    #         setattr(obj, "material_type_name", obj.material_type.name)
    #
    #     return data


class MaterialShortResponse(MaterialResponseBase):
    material_type: "MaterialTypeShortResponse"
    name: str


class MaterialDetailResponse(MaterialResponseBase, ReferenceEntitySchemaMetadataMixin):
    material_type: "MaterialTypeShortResponse"
    name: str


class MaterialListItemResponse(MaterialShortResponse, ReferenceEntitySchemaMetadataMixin):
    pass


class MaterialPaginatedListResponse(PaginatedListResponseBase[MaterialListItemResponse]):
    pass
