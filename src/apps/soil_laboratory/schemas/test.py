from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.soil_laboratory.enums import TestStatus, TestType
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.sample import SampleShortResponse


class TestInputBase(InputBase):
    pass


class TestCreate(TestInputBase):
    sample_id: UUID = Field(alias="sampleId")

    type_: TestType = Field(alias="type")

    measurement_1: float = Field(alias="measurement1")


class TestUpdate(TestInputBase):
    measurement_1: float = Field(None, alias="measurement1")


class TestResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID


class TestLookupResponse(TestResponseBase):
    type_: TestType = Field(alias="type")
    mean_measurement: float = Field(alias="meanMeasurement")
    status: TestStatus


class TestShortResponse(TestResponseBase):
    type_: TestType = Field(alias="type")
    mean_measurement: float = Field(alias="meanMeasurement")
    status: TestStatus


class TestDetailResponse(TestResponseBase, BusinessEntitySchemaMetadataMixin):
    type_: TestType = Field(alias="type")

    sample: "SampleShortResponse"

    measurement_1: float = Field(alias="measurement1")
    measurement_2: float = Field(alias="measurement2")
    measurement_3: float | None = Field(alias="measurement3")

    selected_measurement_1: float = Field(alias="selected_measurement1")
    selected_measurement_2: float = Field(alias="selected_measurement2")

    difference_percent: float = Field(alias="differencePercent")
    mean_measurement: float = Field(alias="meanMeasurement")

    lower_limit: float = Field(alias="lowerLimit")
    upper_limit: float = Field(alias="upperLimit")

    status: TestStatus


class TestListItemResponse(TestShortResponse, BusinessEntitySchemaMetadataMixin):
    pass


class TestListResponse(PaginatedListResponseBase[TestListItemResponse]):
    pass
