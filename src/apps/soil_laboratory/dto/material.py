from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class MaterialCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    material_type_id: UUID
    name: str


class MaterialUpdateDTO(UpdateDTOBase):
    material_type_id: UUID | None = None
    name: str | None = None
