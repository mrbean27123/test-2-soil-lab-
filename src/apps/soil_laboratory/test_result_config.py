from enum import Enum


class SpecialMaterials(str, Enum):
    MS_13 = "13"
    MS_14 = "14"
    MS_15 = "15"

    MCMS_8 = "8"
    MCMS_1C = "1C"
    MCMS_1XC = "1XC"
    MCMS_1C1C = "1C1C"
    MCMS_1C2C = "1C2C"


TEMPERATURE_DEPENDANT_MATERIAL_SPECIFICATIONS = {
    ("molding_sand", "13", "molding_sand_mixer"): {">=+18": (2.60, 3.10), "<+18": (2.50, 3.00)},
    ("molding_sand", "14", "molding_sand_mixer"): {">=+18": (3.40, 3.70), "<+18": (3.30, 3.50)},
    ("molding_sand", "15", "molding_sand_mixer"): {">=+18": (2.60, 3.10), "<+18": (2.50, 3.00)},
    ("molding_sand", "8", "mold_core_workplace"): {">=+18": (4.70, 6.00), "<+18": (4.70, 5.00)},
    ("molding_sand", "8", "mold_core_production"): {">=+18": (4.70, 6.00), "<+18": (4.70, 5.00)}
}

SPECIAL_MATERIAL_SPECIFICATIONS = {
    ("molding_sand_material", "bentonite", "incoming_inspection"): {
        "sieve_0_4_mm_percent": (None, 3.00), "sieve_0_16_mm_percent": (None, 10.00)
    },
    ("mold_core_material", "iron_oxide", "incoming_inspection"): {
        "additiv_hsp_70": (2.80, 3.20), "iron_oxide_type_h400": (2.60, 3.20)
    },
    ("dye_material", "periclase_chromite_powder", "shop_floor"): {
        "sum_sieves_2_5_mm_1_6_mm_1_0_mm_percent": (None, 0.00),
        "sum_sieves_0_63_mm_0_4_mm_0_315_mm_percent": (None, 40.00),
        "sum_sieves_0_063_mm_0_05_mm_pan_percent": (None, 60.00)
    },
}
