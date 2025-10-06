from enum import Enum


class TestType(str, Enum):
    STRENGTH = "strength"
    STRENGTH_AFTER_1_hour = "strength_after_1_hour"
    STRENGTH_AFTER_3_hours = "strength_after_3_hours"
    STRENGTH_AFTER_24_hours = "strength_after_24_hours"
    GAS_PERMEABILITY = "gas_permeability"
    MOISTURE_PERCENT = "moisture_percent"
    GAS_FORMING_PROPERTY = "gas_forming_property"


class TestStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
