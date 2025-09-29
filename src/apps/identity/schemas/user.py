from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from apps.identity.dto import UserCreateDTO, UserUpdateDTO
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin, SoftDeleteMetadataSchemaMixin
from validation.common import validate_person_full_name_part
from validation.contact import validate_email


if TYPE_CHECKING:
    from apps.identity.schemas import PermissionDetailResponse, RoleDetailResponse

PERSON_FIRST_NAME_CONSTRAINTS = {"min_length": 2, "max_length": 50}
PERSON_LAST_NAME_CONSTRAINTS = {"min_length": 2, "max_length": 100}


class UserInputBase(InputBase):
    @field_validator("first_name", "last_name", mode="after", check_fields=False)
    @classmethod
    def validate_full_name_fields(cls, value: str) -> str:
        return validate_person_full_name_part(value)

    @field_validator("email", mode="after", check_fields=False)
    @classmethod
    def validate_email(cls, value: str) -> str:
        return validate_email(value)


class UserCreate(UserInputBase):
    first_name: str = Field(..., **PERSON_FIRST_NAME_CONSTRAINTS, alias="firstName")
    last_name: str = Field(..., **PERSON_LAST_NAME_CONSTRAINTS, alias="lastName")

    email: EmailStr
    raw_password: str = Field(alias="rawPassword")

    is_active: bool = Field(True, alias="isActive")
    is_superuser: bool = Field(False, alias="isSuperuser")

    role_ids: list[UUID] | None = Field(None, alias="roleIds")
    permission_ids: list[UUID] | None = Field(None, alias="permissionIds")

    def to_dto(self) -> UserCreateDTO:
        return UserCreateDTO(**self.model_dump(exclude={"role_ids", "permission_ids"}))


class UserUpdate(UserInputBase):
    first_name: str = Field(None, **PERSON_FIRST_NAME_CONSTRAINTS, alias="firstName")
    last_name: str = Field(None, **PERSON_LAST_NAME_CONSTRAINTS, alias="lastName")

    email: EmailStr = Field(None)

    is_active: bool = Field(None, alias="isActive")
    is_superuser: bool = Field(None, alias="isSuperuser")

    role_ids: list[UUID] = Field(None, alias="roleIds")
    permission_ids: list[UUID] = Field(None, alias="permissionIds")

    def to_dto(self) -> UserUpdateDTO:
        return UserUpdateDTO(
            **self.model_dump(exclude={"role_ids", "permission_ids"}, exclude_unset=True)
        )


class UserResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID


class UserLookupResponse(UserResponseBase):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

    email: str

    is_active: bool = Field(alias="isActive")
    is_superuser: bool = Field(alias="isSuperuser")


class UserShortResponse(UserResponseBase):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

    email: str

    is_active: bool = Field(alias="isActive")
    is_superuser: bool = Field(alias="isSuperuser")


class UserDetailResponse(UserResponseBase, BusinessEntitySchemaMetadataMixin):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

    email: EmailStr

    is_active: bool = Field(alias="isActive")
    is_superuser: bool = Field(alias="isSuperuser")

    last_login_at: datetime | None = Field(None, alias="lastLoginAt")

    roles: list["RoleDetailResponse"]
    permissions: list["PermissionDetailResponse"]


class UserListItemResponse(UserResponseBase, SoftDeleteMetadataSchemaMixin):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

    email: EmailStr

    is_active: bool = Field(alias="isActive")
    is_superuser: bool = Field(alias="isSuperuser")

    last_login_at: datetime | None = Field(None, alias="lastLoginAt")

    roles: list["RoleDetailResponse"]
    permissions: list["PermissionDetailResponse"]


class UserListResponse(PaginatedListResponseBase[UserListItemResponse]):
    pass
