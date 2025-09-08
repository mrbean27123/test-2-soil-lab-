from validation.internal import patterns


def assert_iso_alpha2_is_valid(value: str) -> None:
    if not patterns.ISO_ALPHA2.fullmatch(value):
        raise ValueError("Must be exactly 2 (two) uppercase letters (A-Z)")


def assert_iso_alpha3_is_valid(value: str) -> None:
    if not patterns.ISO_ALPHA3.fullmatch(value):
        raise ValueError("Must be exactly 3 (three) uppercase letters (A-Z)")


def assert_iso_numeric_is_valid(value: str) -> None:
    if not patterns.ISO_NUMERIC.fullmatch(value):
        raise ValueError("Must consist of exactly 3 (three) digits (000–999)")
