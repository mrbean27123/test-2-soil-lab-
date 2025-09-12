from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.soil_laboratory.dto.measurement import MeasurementCreateDTO, MeasurementUpdateDTO
from schemas.base import InputBase, PaginatedListResponseBase
from schemas.mixins import BusinessEntitySchemaMetadataMixin
from validation.common import validate_description


MOLDING_SAND_NUMBER_CONSTRAINTS = {"min_length": 1, "max_length": 50}
MOLDING_SAND_STRENGTH_CONSTRAINTS = {"gt": 0.1, "lt": 5}
MOLDING_SAND_GAS_PERMEABILITY_CONSTRAINTS = {"gt": 50, "lt": 250}
MOLDING_SAND_MOISTURE_PERCENT_CONSTRAINTS = {"gt": 0.1, "lt": 5}
NOTE_CONSTRAINTS = {"min_length": 1, "max_length": 1000}


class MeasurementInputBase(InputBase):
    @field_validator("molding_sand_number", mode="after", check_fields=False)
    @classmethod
    def validate_molding_sand_number(cls, value: str) -> str:
        return value

    @field_validator("note", mode="after", check_fields=False)
    @classmethod
    def validate_note(cls, value: str | None) -> str | None:
        return (
            validate_description(value, only_ukrainian_letters=False)
            if value is not None else value
        )


class MeasurementCreate(MeasurementInputBase):
    molding_sand_number: str = Field(..., **MOLDING_SAND_NUMBER_CONSTRAINTS)

    molding_sand_strength_kgf_cm2: float = Field(..., **MOLDING_SAND_STRENGTH_CONSTRAINTS)
    molding_sand_gas_permeability: float = Field(..., **MOLDING_SAND_GAS_PERMEABILITY_CONSTRAINTS)
    molding_sand_moisture_percent: float = Field(..., **MOLDING_SAND_MOISTURE_PERCENT_CONSTRAINTS)

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> MeasurementCreateDTO:
        return MeasurementCreateDTO(**self.model_dump())


class MeasurementUpdate(MeasurementInputBase):
    molding_sand_number: str = Field(None, **MOLDING_SAND_NUMBER_CONSTRAINTS)

    molding_sand_strength_kgf_cm2: float = Field(None, **MOLDING_SAND_STRENGTH_CONSTRAINTS)
    molding_sand_gas_permeability: float = Field(None, **MOLDING_SAND_GAS_PERMEABILITY_CONSTRAINTS)
    molding_sand_moisture_percent: float = Field(None, **MOLDING_SAND_MOISTURE_PERCENT_CONSTRAINTS)

    note: str | None = Field(None, **NOTE_CONSTRAINTS)

    def to_dto(self) -> MeasurementUpdateDTO:
        return MeasurementUpdateDTO(**self.model_dump(exclude_unset=True))


class MeasurementResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class MeasurementLookupResponse(MeasurementResponseBase):
    molding_sand_number: str

    molding_sand_strength_kgf_cm2: float
    molding_sand_gas_permeability: float
    molding_sand_moisture_percent: float


class MeasurementShortResponse(MeasurementResponseBase):
    molding_sand_number: str

    molding_sand_strength_kgf_cm2: float
    molding_sand_gas_permeability: float
    molding_sand_moisture_percent: float


class MeasurementDetailResponse(MeasurementResponseBase, BusinessEntitySchemaMetadataMixin):
    molding_sand_number: str

    molding_sand_strength_kgf_cm2: float
    molding_sand_gas_permeability: float
    molding_sand_moisture_percent: float

    note: str | None


class MeasurementListItemResponse(MeasurementShortResponse, BusinessEntitySchemaMetadataMixin):
    pass


class MeasurementListResponse(PaginatedListResponseBase[MeasurementListItemResponse]):
    pass


class MeasurementsReportGenerationRequest(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class MeasurementsReportGenerationResponse(BaseModel):
    success: bool
    message: str
    file_name: str
    total_records: int
    generated_at: datetime
