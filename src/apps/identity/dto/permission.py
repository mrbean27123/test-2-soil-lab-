from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class PermissionCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    code: str
    name: str
    description: str | None = None


class PermissionUpdateDTO(UpdateDTOBase):
    code: str | None = None
    name: str | None = None
    description: str | None = None
