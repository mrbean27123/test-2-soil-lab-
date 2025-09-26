from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.soil_laboratory.dto.test import TestCreateDTO, TestUpdateDTO
from apps.soil_laboratory.enums import TestStatus, TestType
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.sample import SampleShortResponse


class TestInputBase(InputBase):
    pass


class TestCreate(TestInputBase):
    sample_id: UUID

    type_: TestType

    measurement_1: float


class TestUpdate(TestInputBase):
    measurement_1: float = Field(None)


class TestResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class TestLookupResponse(TestResponseBase):
    type_: TestType
    mean_measurement: float
    status: TestStatus


class TestShortResponse(TestResponseBase):
    type_: TestType
    mean_measurement: float
    status: TestStatus


class TestDetailResponse(TestResponseBase, BusinessEntitySchemaMetadataMixin):
    type_: TestType

    sample: "SampleShortResponse"

    measurement_1: float
    measurement_2: float
    measurement_3: float | None

    selected_measurement_1: float
    selected_measurement_2: float

    difference_percent: float
    mean_measurement: float

    lower_limit: float
    upper_limit: float

    status: TestStatus


class TestListItemResponse(TestShortResponse, BusinessEntitySchemaMetadataMixin):
    pass


class TestListResponse(PaginatedListResponseBase[TestListItemResponse]):
    pass
