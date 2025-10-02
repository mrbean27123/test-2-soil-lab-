from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict, Field

from apps.soil_laboratory.enums import TestStatus, TestType
from schemas.base import InputSchemaBase, PaginatedListResponseBase, SchemaBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.sample import SampleShortResponse


class TestInputSchemaBase(InputSchemaBase):
    pass


class TestCreate(TestInputSchemaBase):
    sample_id: UUID

    type_: TestType = Field(alias="type")
    measurement_1: float


class TestUpdate(TestInputSchemaBase):
    measurement_1: float = Field(None)


class TestResponseBase(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class TestLookupResponse(TestResponseBase):
    type_: TestType = Field(alias="type")
    mean_measurement: float
    status: TestStatus


class TestShortResponse(TestResponseBase):
    type_: TestType = Field(alias="type")
    mean_measurement: float
    status: TestStatus


class TestDetailResponse(TestResponseBase, BusinessEntitySchemaMetadataMixin):
    type_: TestType = Field(alias="type")

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
