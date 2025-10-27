from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class ParameterCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    name: str
    units: str


class ParameterUpdateDTO(UpdateDTOBase):
    name: str | None = None
    units: str | None = None
