from datetime import datetime

from dto import CreateDTOBase, UpdateDTOBase


class SampleCreateDTO(CreateDTOBase):
    molding_sand_recipe: str
    received_at: datetime

    note: str | None = None


class SampleUpdateDTO(UpdateDTOBase):
    molding_sand_recipe: str | None = None
    received_at: datetime | None = None

    note: str | None = None
