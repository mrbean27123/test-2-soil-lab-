from typing import Any, TYPE_CHECKING
from uuid import UUID

from pydantic import Json

from schemas.base import InputSchemaBase, PaginatedListResponseBase, ResponseSchemaBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin


if TYPE_CHECKING:
    from apps.soil_laboratory.schemas.measurement import MeasurementShortResponse
    from apps.soil_laboratory.schemas.parameter import ParameterShortResponse
    from apps.soil_laboratory.schemas.sample import SampleShortResponse


class TestInputSchemaBase(InputSchemaBase):
    pass


class TestResultCreate(TestInputSchemaBase):
    sample_id: UUID
    parameter_id: UUID

    measurements: list[float] | None = None
    context: Json[dict[str, Any]] | None = None


class TestResultUpdate(TestInputSchemaBase):
    pass


TestResultResponseBase = ResponseSchemaBase[UUID]


class TestResultLookupResponse(TestResultResponseBase):
    sample: "SampleShortResponse"
    parameter: "ParameterShortResponse"

    mean_value: float | None
    variation_percentage: float | None

    is_compliant: bool


class TestResultShortResponse(TestResultResponseBase):
    parameter: "ParameterShortResponse"

    mean_value: float | None
    variation_percentage: float | None

    is_compliant: bool


class TestResultDetailResponse(TestResultResponseBase, BusinessEntitySchemaMetadataMixin):
    sample: "SampleShortResponse"
    parameter: "ParameterShortResponse"

    measurements: list["MeasurementShortResponse"]

    mean_value: float | None
    variation_percentage: float | None

    lower_limit: float | None
    upper_limit: float | None

    is_compliant: bool


class TestResultListItemResponse(TestResultLookupResponse, BusinessEntitySchemaMetadataMixin):
    pass


class TestResultPaginatedListResponse(PaginatedListResponseBase[TestResultListItemResponse]):
    pass
