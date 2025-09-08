from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.identity.dto import RoleCreateDTO, RoleUpdateDTO
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import ReferenceEntitySchemaMetadataMixin
from validation.common import validate_description, validate_entity_name


if TYPE_CHECKING:
    from apps.identity.schemas import PermissionShortResponse

ROLE_CODE_CONSTRAINTS = {"min_length": 5, "max_length": 255}
ROLE_NAME_CONSTRAINTS = {"min_length": 2, "max_length": 120}
ROLE_DESCRIPTION_CONSTRAINTS = {"min_length": 5, "max_length": 255}


class RoleInputBase(InputBase):
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
        return validate_description(value) if value is not None else value


class RoleCreate(RoleInputBase):
    code: str = Field(..., **ROLE_CODE_CONSTRAINTS)
    name: str = Field(..., **ROLE_NAME_CONSTRAINTS)
    description: str | None = Field(None, **ROLE_DESCRIPTION_CONSTRAINTS)

    permission_ids: list[UUID] | None = None

    def to_dto(self) -> RoleCreateDTO:
        return RoleCreateDTO(**self.model_dump(exclude={"permission_ids", }))


class RoleUpdate(RoleInputBase):
    code: str = Field(None, **ROLE_CODE_CONSTRAINTS)
    name: str = Field(None, **ROLE_NAME_CONSTRAINTS)
    description: str | None = Field(None, **ROLE_DESCRIPTION_CONSTRAINTS)

    permission_ids: list[UUID] = Field(None)

    def to_dto(self) -> RoleUpdateDTO:
        return RoleUpdateDTO(**self.model_dump(exclude={"permission_ids", }, exclude_unset=True))


class RoleResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class RoleLookupResponse(RoleResponseBase):
    code: str
    name: str


class RoleShortResponse(RoleResponseBase):
    code: str
    name: str


class RoleDetailResponse(RoleResponseBase, ReferenceEntitySchemaMetadataMixin):
    code: str
    name: str
    description: str | None = None

    permissions: list["PermissionShortResponse"]


class RoleListItemResponse(RoleResponseBase, ReferenceEntitySchemaMetadataMixin):
    code: str
    name: str

    permissions: list["PermissionShortResponse"]


class RoleListResponse(PaginatedListResponseBase[RoleListItemResponse]):
    pass
