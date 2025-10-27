from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class SpecificationCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    parameter_id: UUID
    material_id: UUID
    material_source_id: UUID

    min_value: float | None
    max_value: float | None


class SpecificationUpdateDTO(UpdateDTOBase):
    parameter_id: UUID | None = None
    material_id: UUID | None = None
    material_source_id: UUID | None = None

    min_value: float | None = None
    max_value: float | None = None
