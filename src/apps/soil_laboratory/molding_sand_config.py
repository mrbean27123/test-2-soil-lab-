from enum import Enum


class MoldingSandRecipes(str, Enum):
    MS_13 = "13"
    MS_14 = "14"
    MS_15 = "15"


STRENGTH_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MS_13.value: (1.05, 1.2),
    MoldingSandRecipes.MS_14.value: (1.2, 1.3),
    MoldingSandRecipes.MS_15.value: (1.05, 1.2)
}

GAS_PERMEABILITY_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MS_13.value: (100, 1000),
    MoldingSandRecipes.MS_14.value: (100, 1000),
    MoldingSandRecipes.MS_15.value: (100, 1000)
}

MOISTURE_CONSTRAINTS: dict[str, tuple[float, float]] = {
    MoldingSandRecipes.MS_13.value: (2.6, 3.1),
    MoldingSandRecipes.MS_14.value: (3.4, 3.7),
    MoldingSandRecipes.MS_15.value: (2.6, 3.1)
}
