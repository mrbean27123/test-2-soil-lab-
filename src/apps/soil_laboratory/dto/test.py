from uuid import UUID

from apps.soil_laboratory.enums import TestStatus, TestType
from dto import CreateDTOBase, UpdateDTOBase


class TestCreateDTO(CreateDTOBase):
    sample_id: UUID

    type_: TestType

    measurement_1: float
    measurement_2: float
    measurement_3: float | None = None

    selected_measurement_1: float
    selected_measurement_2: float

    difference_percent: float
    mean_measurement: float

    lower_limit: float
    upper_limit: float

    status: TestStatus


class TestUpdateDTO(UpdateDTOBase):
    measurement_1: float | None = None
