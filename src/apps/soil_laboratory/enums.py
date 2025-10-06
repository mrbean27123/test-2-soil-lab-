from enum import Enum


class TestType(str, Enum):
    COMPRESSIVE_STRENGTH = "compressive_strength"
    TENSILE_STRENGTH = "tensile_strength"
    TENSILE_STRENGTH_AFTER_0_hours = "tensile_strength_after_0_hours"
    TENSILE_STRENGTH_AFTER_1_hour = "tensile_strength_after_1_hour"
    TENSILE_STRENGTH_AFTER_3_hours = "tensile_strength_after_3_hours"
    TENSILE_STRENGTH_AFTER_24_hours = "tensile_strength_after_24_hours"
    GAS_PERMEABILITY = "gas_permeability"
    MOISTURE_PERCENT = "moisture_percent"
    GAS_FORMING_PROPERTY = "gas_forming_property"


class TestStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
