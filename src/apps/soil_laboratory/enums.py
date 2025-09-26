from enum import Enum


class TestType(str, Enum):
    STRENGTH = "strength"
    GAS_PERMEABILITY = "gas_permeability"
    MOISTURE_PERCENT = "moisture_percent"


class TestStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
