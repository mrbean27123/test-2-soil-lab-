from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class MaterialTypeCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)
    name: str


class MaterialTypeUpdateDTO(UpdateDTOBase):
    name: str | None = None
