from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from dto import CreateDTOBase, UpdateDTOBase


class SampleCreateDTO(CreateDTOBase):
    id: UUID = Field(default_factory=uuid4)

    material_id: UUID
    material_source_id: UUID

    temperature: float
    received_at: datetime

    note: str | None = None


class SampleUpdateDTO(UpdateDTOBase):
    received_at: datetime | None = None

    note: str | None = None
