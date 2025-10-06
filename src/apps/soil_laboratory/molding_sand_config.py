from enum import Enum


class MoldingSandRecipes(str, Enum):
    MS_13 = "13"
    MS_14 = "14"
    MS_15 = "15"

    MCMS_8 = "8"
    MCMS_1C = "1C"
    MCMS_1XC = "1XC"
    MCMS_1C1C = "1C1C"
    MCMS_1C2C = "1C2C"


STRENGTH_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MS_13.value: (1.05, 1.2),
    MoldingSandRecipes.MS_14.value: (1.2, 1.3),
    MoldingSandRecipes.MS_15.value: (1.05, 1.2),

    MoldingSandRecipes.MCMS_8.value: (0.15, 10.0),
    MoldingSandRecipes.MCMS_1C.value: (0.44, 10.0),
    MoldingSandRecipes.MCMS_1XC.value: (0.44, 10.0),
    MoldingSandRecipes.MCMS_1C1C.value: (0.44, 10.0),
    MoldingSandRecipes.MCMS_1C2C.value: (0.44, 10.0),
}

GAS_PERMEABILITY_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MS_13.value: (100, 1000),
    MoldingSandRecipes.MS_14.value: (100, 1000),
    MoldingSandRecipes.MS_15.value: (100, 1000),

    MoldingSandRecipes.MCMS_8.value: (100, 1000),
}

MOISTURE_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MS_13.value: (2.6, 3.1),
    MoldingSandRecipes.MS_14.value: (3.4, 3.7),
    MoldingSandRecipes.MS_15.value: (2.6, 3.1),

    MoldingSandRecipes.MCMS_8.value: (4.7, 6.0),
}

GAS_FORMING_PROPERTY_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MCMS_1C.value: (0.01, 14.0),
    MoldingSandRecipes.MCMS_1XC.value: (0.01, 14.0),
    MoldingSandRecipes.MCMS_1C1C.value: (0.01, 14.0),
    MoldingSandRecipes.MCMS_1C2C.value: (0.01, 14.0),
}
