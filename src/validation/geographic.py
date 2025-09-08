from typing import Literal

from validation.internal.codes import (
    assert_iso_alpha2_is_valid,
    assert_iso_alpha3_is_valid,
    assert_iso_numeric_is_valid
)
from validation.internal.text import (
    assert_all_letters_are_ukrainian,
    assert_full_address_is_valid,
    assert_postal_code_is_valid,
    assert_text_contains_only_allowed_characters,
    assert_text_starts_with_capital_letter,
    assert_valid_word_boundaries
)
from validation.internal.utils import normalize_whitespace


def validate_geographical_name(
    value: str,
    require_capital: bool = True,
    only_ukrainian_letters: bool = True
) -> str:
    value = normalize_whitespace(value)

    assert_text_contains_only_allowed_characters(value)
    assert_valid_word_boundaries(value)

    if require_capital:
        assert_text_starts_with_capital_letter(value)

    if only_ukrainian_letters:
        assert_all_letters_are_ukrainian(value)

    return value


def validate_iso_alpha(value: str, alpha_type: int = Literal[2, 3]) -> str:
    if alpha_type == 2:
        assert_iso_alpha2_is_valid(value)
    elif alpha_type == 3:
        assert_iso_alpha3_is_valid(value)
    else:
        raise ValueError("Only ISO Alpha 2 & 3 are supported")

    return value


def validate_iso_numeric(value: str) -> str:
    assert_iso_numeric_is_valid(value)

    return value


def validate_address(value: str, only_ukrainian_letters: bool = True) -> str:
    value = normalize_whitespace(value)

    assert_full_address_is_valid(value)

    if only_ukrainian_letters:
        assert_all_letters_are_ukrainian(value)

    return value


def validate_postal_code(value: str) -> str:
    value = value.upper()

    assert_postal_code_is_valid(value)

    return value
