from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class TestResultCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    sample_id: UUID
    parameter_id: UUID

    mean_value: float | None
    variation_percentage: float | None

    lower_limit: float | None
    upper_limit: float | None

    is_compliant: bool


class TestResultUpdateDTO(UpdateDTOBase):
    sample_id: UUID | None = None
    parameter_id: UUID | None = None

    mean_value: float | None = None
    variation_percentage: float | None = None

    lower_limit: float | None = None
    upper_limit: float | None = None

    is_compliant: bool | None = None
