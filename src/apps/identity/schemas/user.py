from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict, EmailStr, Field, field_validator

from apps.identity.dto import UserCreateDTO, UserUpdateDTO
from schemas.base import InputSchemaBase, PaginatedListResponseBase, SchemaBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin, SoftDeleteMetadataSchemaMixin
from validation.common import validate_person_full_name_part
from validation.contact import validate_email


if TYPE_CHECKING:
    from apps.identity.schemas import PermissionDetailResponse, RoleDetailResponse

PERSON_FIRST_NAME_CONSTRAINTS = {"min_length": 2, "max_length": 50}
PERSON_LAST_NAME_CONSTRAINTS = {"min_length": 2, "max_length": 100}


class UserInputSchemaBase(InputSchemaBase):
    @field_validator("first_name", "last_name", mode="after", check_fields=False)
    @classmethod
    def validate_full_name_fields(cls, value: str) -> str:
        return validate_person_full_name_part(value)

    @field_validator("email", mode="after", check_fields=False)
    @classmethod
    def validate_email(cls, value: str) -> str:
        return validate_email(value)


class UserCreate(UserInputSchemaBase):
    first_name: str = Field(..., **PERSON_FIRST_NAME_CONSTRAINTS)
    last_name: str = Field(..., **PERSON_LAST_NAME_CONSTRAINTS)

    email: EmailStr
    raw_password: str

    is_active: bool = True
    is_superuser: bool = False

    role_ids: list[UUID] | None = None
    permission_ids: list[UUID] | None = None

    def to_dto(self) -> UserCreateDTO:
        return UserCreateDTO(**self.model_dump(exclude={"role_ids", "permission_ids"}))


class UserUpdate(UserInputSchemaBase):
    first_name: str = Field(None, **PERSON_FIRST_NAME_CONSTRAINTS)
    last_name: str = Field(None, **PERSON_LAST_NAME_CONSTRAINTS)

    email: EmailStr = Field(None)

    is_active: bool = Field(None)
    is_superuser: bool = Field(None)

    role_ids: list[UUID] = Field(None)
    permission_ids: list[UUID] = Field(None)

    def to_dto(self) -> UserUpdateDTO:
        return UserUpdateDTO(
            **self.model_dump(exclude={"role_ids", "permission_ids"}, exclude_unset=True)
        )


class UserResponseBase(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class UserLookupResponse(UserResponseBase):
    first_name: str
    last_name: str

    email: str

    is_active: bool
    is_superuser: bool


class UserShortResponse(UserResponseBase):
    first_name: str
    last_name: str

    email: str

    is_active: bool
    is_superuser: bool


class UserDetailResponse(UserResponseBase, BusinessEntitySchemaMetadataMixin):
    first_name: str
    last_name: str

    email: EmailStr

    is_active: bool
    is_superuser: bool

    last_login_at: datetime | None

    roles: list["RoleDetailResponse"]
    permissions: list["PermissionDetailResponse"]


class UserListItemResponse(UserResponseBase, SoftDeleteMetadataSchemaMixin):
    first_name: str
    last_name: str

    email: EmailStr

    is_active: bool
    is_superuser: bool

    last_login_at: datetime | None

    roles: list["RoleDetailResponse"]
    permissions: list["PermissionDetailResponse"]


class UserListResponse(PaginatedListResponseBase[UserListItemResponse]):
    pass
