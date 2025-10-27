from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class MeasurementCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    test_result_id: UUID
    value: float


class MeasurementUpdateDTO(UpdateDTOBase):
    value: float | None = None
