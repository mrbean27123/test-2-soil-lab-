from dto import CreateDTOBase, UpdateDTOBase


class MeasurementCreateDTO(CreateDTOBase):
    molding_sand_number: str

    molding_sand_strength_kgf_cm2: float
    molding_sand_gas_permeability: float
    molding_sand_moisture_percent: float

    note: str | None = None


class MeasurementUpdateDTO(UpdateDTOBase):
    molding_sand_number: str | None = None

    molding_sand_strength_kgf_cm2: float | None = None
    molding_sand_gas_permeability: float | None = None
    molding_sand_moisture_percent: float | None = None

    note: str | None = None
