from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class UserCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    first_name: str
    last_name: str

    email: str
    raw_password: str

    is_active: bool
    is_superuser: bool


class UserUpdateDTO(UpdateDTOBase):
    first_name: str | None = None
    last_name: str | None = None

    email: str | None = None

    is_active: bool | None = None
    is_superuser: bool | None = None
