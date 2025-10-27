from typing import Any

from apps.soil_laboratory.dto.test_result import TestResultCreateDTO
from apps.soil_laboratory.models import Parameter, Sample, Specification
from apps.soil_laboratory.schemas.test_result import TestResultCreate


TEMPERATURE_DEPENDANT_MATERIAL_SPECIFICATIONS = {
    # (parameter.code, material_type.code, material.name, material_source.code): ...
    ("moisture", "molding_sand", "№13 (наповнювальна)", "sand_mixer"): (
        {">=18": (2.60, 3.10), "<18": (2.50, 3.00)}
    ),
    ("moisture", "molding_sand", "№14 (облицювальна)", "sand_mixer"): (
        {">=18": (3.40, 3.70), "<18": (3.30, 3.50)}
    ),
    ("moisture", "molding_sand", "№15 (для освіження)", "sand_mixer"): (
        {">=18": (2.60, 3.10), "<18": (2.50, 3.00)}
    ),

    ("moisture", "molding_sand", "№8", "workplace"): {">=18": (4.70, 6.00), "<18": (4.70, 5.00)},
    ("moisture", "molding_sand", "№8", "sand_mixer"): {">=18": (4.70, 6.00), "<18": (4.70, 5.00)},

    ("temperature", "molding_sand_material", "пісок формувальний", "storage_hopper"): (
        {">=18": (20.00, 40.00), "<18": (10.00, 40.00)}
    )
}

SPECIAL_MATERIAL_SPECIFICATIONS = {
    # (parameter.code, material_type.code, material.name, material_source.code): ...
    ("granulometric_composition", "molding_sand_material", "бентоніт", "incoming_inspection"): {
        "sieve_0_4_mm_percent": (None, 3.00), "sieve_0_16_mm_percent": (None, 10.00)
    },
    ("bulk_density", "mold_core_material", "оксид заліза", "incoming_inspection"): {
        "additiv_hsp_70": (2.80, 3.20), "iron_oxide_type_h400": (2.60, 3.20)
    },
    (
        "granulometric_composition",
        "mold_core_coating_material",
        "порошок периклазохромітовий (ппхт)",
        "shop"
    ): {
        "sum_sieves_2_5_mm_1_6_mm_1_0_mm_percent": (None, 0.00),
        "sum_sieves_0_63_mm_0_4_mm_0_315_mm_percent": (None, 40.00),
        "sum_sieves_0_063_mm_0_05_mm_pan_percent": (None, 60.00)
    }
}


def _check_value_in_limits(value: float, limits: tuple[float | None, float | None]) -> bool:
    lower_limit, upper_limit = limits

    check_lower = (lower_limit is None) or (value >= lower_limit)
    check_upper = (upper_limit is None) or (value <= upper_limit)

    return check_lower and check_upper


def _visual_test_case(
    sample: Sample,
    parameter: Parameter,
    test_result_data: TestResultCreate
) -> TestResultCreateDTO | None:
    if not parameter.code == "appearance":
        return None

    test_result_context = test_result_data.context
    is_visual_test_compliant = (
        test_result_context.get("is_visual_test_compliant") if test_result_context else None
    )

    if not test_result_context or is_visual_test_compliant is None:
        raise ValueError("No visual test context provided")

    return TestResultCreateDTO(
        sample_id=sample.id,
        parameter_id=test_result_data.parameter_id,

        mean_value=None,
        variation_percentage=None,

        lower_limit=None,
        upper_limit=None,

        is_compliant=is_visual_test_compliant
    )


def _base_case(
    sample: Sample,
    parameter: Parameter,
    test_result_data: TestResultCreate,
    specification: Specification
) -> TestResultCreateDTO | None:
    lower_limit, upper_limit = ..., ...

    if specification:
        lower_limit, upper_limit = specification.min_value, specification.max_value
    else:
        temperature_specification_key = (
            parameter.code,
            sample.material.material_type.code,
            sample.material.name.lower(),
            sample.material_source.code
        )
        specification = TEMPERATURE_DEPENDANT_MATERIAL_SPECIFICATIONS.get(
            temperature_specification_key
        )

        if specification:
            lower_limit, upper_limit = (
                specification[">=18"] if sample.temperature >= 18 else specification["<18"]
            )

    if lower_limit is ... or upper_limit is ...:
        return None

    if not test_result_data.measurements:
        raise ValueError("No measurements provided")

    mean_measurement_value = test_result_data.measurements[0]
    variation_percentage = 0

    is_test_compliant = _check_value_in_limits(mean_measurement_value, (lower_limit, upper_limit))

    return TestResultCreateDTO(
        sample_id=sample.id,
        parameter_id=test_result_data.parameter_id,

        mean_value=mean_measurement_value,
        variation_percentage=variation_percentage,

        lower_limit=lower_limit,
        upper_limit=upper_limit,

        is_compliant=is_test_compliant
    )


def _special_test_case(
    sample: Sample,
    parameter: Parameter,
    test_result_data: TestResultCreate
) -> TestResultCreateDTO | None:
    test_result_context = test_result_data.context

    if not test_result_context:
        return None

    specification_key = (
        parameter.code,
        sample.material.material_type.code,
        sample.material.name.lower(),
        sample.material_source.code
    )

    specification = SPECIAL_MATERIAL_SPECIFICATIONS.get(specification_key)

    if not specification:
        return None

    match sample.material.name.lower():
        case "бентоніт":
            return _calculate_bentonite(sample, test_result_data, specification)
        case "оксид заліза":
            return _calculate_iron_oxide(sample, test_result_data, specification)
        case "порошок периклазохромітовий (ппхт)":
            return _calculate_periclase_chromite_powder(sample, test_result_data, specification)
        case _:
            raise ValueError("Unknown material name for special test")


def _calculate_bentonite(
    sample: Sample,
    test_result_data: TestResultCreate,
    specification: dict[str, Any]
) -> TestResultCreateDTO:
    test_result_context = test_result_data.context

    if not test_result_context:
        raise ValueError("No context provided")

    parameters_to_check = ["sieve_0_4_mm_percent", "sieve_0_16_mm_percent"]

    is_test_compliant = True

    try:
        for param_name in parameters_to_check:
            limits = specification[param_name]

            result_value = test_result_context[param_name]

            if not _check_value_in_limits(result_value, limits):
                is_test_compliant = False
                break

    except KeyError as e:
        raise ValueError(f"Wrong context or specification format. Missing key: {e}")
    except TypeError:
        raise ValueError("Invalid data type for limits or result value.")

    return TestResultCreateDTO(
        sample_id=sample.id,
        parameter_id=test_result_data.parameter_id,

        mean_value=None,
        variation_percentage=None,

        lower_limit=None,
        upper_limit=None,

        is_compliant=is_test_compliant
    )


def _calculate_iron_oxide(
    sample: Sample,
    test_result_data: TestResultCreate,
    specification: dict[str, Any]
) -> TestResultCreateDTO:
    test_result_context = test_result_data.context

    if not test_result_context:
        raise ValueError("No context provided")

    try:
        material_brand = test_result_context["material_brand"]
        lower_limit, upper_limit = specification[material_brand]

        mean_measurement_value = test_result_data.measurements[0]
        variation_percentage = 0

        is_test_compliant = _check_value_in_limits(
            test_result_data.measurements[0],
            (lower_limit, upper_limit)
        )

    except KeyError as e:
        raise ValueError(f"Wrong context or specification format. Missing key: {e}")
    except TypeError:
        raise ValueError("Invalid data type for limits or result value.")

    return TestResultCreateDTO(
        sample_id=sample.id,
        parameter_id=test_result_data.parameter_id,

        mean_value=mean_measurement_value,
        variation_percentage=variation_percentage,

        lower_limit=lower_limit,
        upper_limit=upper_limit,

        is_compliant=is_test_compliant
    )


def _calculate_periclase_chromite_powder(
    sample: Sample,
    test_result_data: TestResultCreate,
    specification: dict[str, Any]
) -> TestResultCreateDTO:
    test_result_context = test_result_data.context

    if not test_result_context:
        raise ValueError("No context provided")

    parameters_to_check = [
        "sum_sieves_2_5_mm_1_6_mm_1_0_mm_percent",
        "sum_sieves_0_63_mm_0_4_mm_0_315_mm_percent",
        "sum_sieves_0_063_mm_0_05_mm_pan_percent"
    ]

    is_test_compliant = True

    try:
        for param_name in parameters_to_check:
            limits = specification[param_name]

            result_value = test_result_context[param_name]

            if not _check_value_in_limits(result_value, limits):
                is_test_compliant = False
                break

    except KeyError as e:
        raise ValueError(f"Wrong context or specification format. Missing key: {e}")
    except TypeError:
        raise ValueError("Invalid data type for limits or result value.")

    return TestResultCreateDTO(
        sample_id=sample.id,
        parameter_id=test_result_data.parameter_id,

        mean_value=None,
        variation_percentage=None,

        lower_limit=None,
        upper_limit=None,

        is_compliant=is_test_compliant
    )


def resolve_strategies_and_get_test_result_create_dto(
    sample: Sample,
    parameter: Parameter,
    test_result_data: TestResultCreate,
    specification: Specification
) -> TestResultCreateDTO:
    result = (
        _visual_test_case(sample, parameter, test_result_data)
        or _base_case(sample, parameter, test_result_data, specification)
        or _special_test_case(sample, parameter, test_result_data)
    )

    if not result:
        raise ValueError("Failed to calculate test result")

    return result
