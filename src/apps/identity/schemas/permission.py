from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.identity.dto import PermissionCreateDTO, PermissionUpdateDTO
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin
from validation.common import (
    validate_description,
    validate_entity_name,
    validate_permission_system_name
)


PERMISSION_CODE_CONSTRAINTS = {"min_length": 5, "max_length": 255}
PERMISSION_NAME_CONSTRAINTS = {"min_length": 2, "max_length": 120}
PERMISSION_DESCRIPTION_CONSTRAINTS = {"min_length": 5, "max_length": 255}


class PermissionInputBase(InputBase):
    @field_validator("code", mode="after", check_fields=False)
    @classmethod
    def validate_code(cls, value: str) -> str:
        return value

    @field_validator("name", mode="after", check_fields=False)
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_entity_name(value)

    @field_validator("description", mode="after", check_fields=False)
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        return (
            validate_description(value, only_ukrainian_letters=False)
            if value is not None else value
        )


class PermissionCreate(PermissionInputBase):
    code: str = Field(..., **PERMISSION_CODE_CONSTRAINTS)
    name: str = Field(..., **PERMISSION_NAME_CONSTRAINTS)
    description: str | None = Field(None, **PERMISSION_DESCRIPTION_CONSTRAINTS)

    def to_dto(self) -> PermissionCreateDTO:
        return PermissionCreateDTO(**self.model_dump())


class PermissionUpdate(PermissionInputBase):
    code: str = Field(None, **PERMISSION_CODE_CONSTRAINTS)
    name: str = Field(None, **PERMISSION_NAME_CONSTRAINTS)
    description: str | None = Field(None, **PERMISSION_DESCRIPTION_CONSTRAINTS)

    def to_dto(self) -> PermissionUpdateDTO:
        return PermissionUpdateDTO(**self.model_dump(exclude_unset=True))


class PermissionResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class PermissionLookupResponse(PermissionResponseBase):
    code: str
    name: str


class PermissionShortResponse(PermissionResponseBase):
    code: str
    name: str


class PermissionDetailResponse(PermissionResponseBase, ReferenceEntitySchemaMetadataMixin):
    code: str
    name: str
    description: str | None = None


class PermissionListItemResponse(PermissionShortResponse, ReferenceEntitySchemaMetadataMixin):
    pass


class PermissionListResponse(PaginatedListResponseBase[PermissionListItemResponse]):
    pass
