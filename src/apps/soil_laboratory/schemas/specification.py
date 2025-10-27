from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from apps.soil_laboratory.dto.specification import SpecificationCreateDTO, SpecificationUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.material import MaterialShortResponse
    from apps.soil_laboratory.schemas.material_source import MaterialSourceShortResponse
    from apps.soil_laboratory.schemas.parameter import ParameterShortResponse


class SpecificationInputSchemaBase(InputSchemaBase):
    pass


class SpecificationCreate(SpecificationInputSchemaBase):
    parameter_id: UUID
    material_id: UUID
    material_source_id: UUID

    min_value: float
    max_value: float

    def to_dto(self) -> SpecificationCreateDTO:
        return SpecificationCreateDTO(**self.model_dump())


class SpecificationUpdate(SpecificationInputSchemaBase):
    parameter_id: UUID = Field(None)
    material_id: UUID = Field(None)
    material_source_id: UUID = Field(None)

    min_value: float = Field(None)
    max_value: float = Field(None)

    def to_dto(self) -> SpecificationUpdateDTO:
        return SpecificationUpdateDTO(**self.model_dump(exclude_unset=True))


SpecificationResponseBase = ResponseSchemaBase[UUID]


class SpecificationLookupResponse(SpecificationResponseBase):
    parameter: "ParameterShortResponse"
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    min_value: float
    max_value: float


class SpecificationShortResponse(SpecificationResponseBase):
    parameter: "ParameterShortResponse"
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    min_value: float
    max_value: float


class SpecificationDetailResponse(SpecificationResponseBase, ReferenceEntitySchemaMetadataMixin):
    parameter: "ParameterShortResponse"
    material: "MaterialShortResponse"
    material_source: "MaterialSourceShortResponse"

    min_value: float
    max_value: float


class SpecificationListItemResponse(SpecificationShortResponse, ReferenceEntitySchemaMetadataMixin):
    pass


class SpecificationPaginatedListResponse(PaginatedListResponseBase[SpecificationListItemResponse]):
    pass
