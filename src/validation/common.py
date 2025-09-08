from datetime import date

from validation.internal.text import (
    assert_all_letters_are_ukrainian,
    assert_text_contains_only_allowed_characters,
    assert_text_is_valid_system_name, assert_text_starts_with_capital_letter,
    assert_valid_word_boundaries
)
from validation.internal.utils import normalize_whitespace


def validate_person_full_name_part(name_part: str, only_ukrainian_letters: bool = True) -> str:
    name_part = normalize_whitespace(name_part)

    assert_text_contains_only_allowed_characters(name_part)
    assert_valid_word_boundaries(name_part)

    assert_text_starts_with_capital_letter(name_part)

    if only_ukrainian_letters:
        assert_all_letters_are_ukrainian(name_part)

    return name_part


def validate_birth_date(birth_date: date, min_age: int = 16, max_age: int = 120) -> date:
    today = date.today()

    if birth_date > today:
        raise ValueError("Birth date cannot be in the future.")

    age = today.year - birth_date.year - (
        # subtract 1 if birthday hasn't occurred yet this year (True == 1, False == 0)
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

    if age < min_age:
        raise ValueError(f"Person must be at least {min_age} years old.")
    if age > max_age:
        raise ValueError(f"Person age cannot exceed {max_age} years.")

    return birth_date


def validate_entity_name(entity_name: str, only_ukrainian_letters: bool = True) -> str:
    return validate_person_full_name_part(entity_name, only_ukrainian_letters)


def validate_permission_system_name(permission_name: str) -> str:
    assert_text_is_valid_system_name(permission_name)

    return permission_name


def validate_description(
    value: str,
    require_capital: bool = True,
    only_ukrainian_letters: bool = True
) -> str:
    value = normalize_whitespace(value)

    if require_capital:
        assert_text_starts_with_capital_letter(value)

    if only_ukrainian_letters:
        assert_all_letters_are_ukrainian(value)

    return value
