import validation.internal.patterns as patterns


def assert_text_contains_only_allowed_characters(text: str) -> None:
    if patterns.FORBIDDEN_NAME_CHARACTERS.search(text):
        raise ValueError("Contains invalid characters")


def assert_text_is_valid_system_name(text: str) -> None:
    if not patterns.SYSTEM_NAME.fullmatch(text):
        raise ValueError(
            "Wrong format. Only lowercase letters (a-z) and underscores (_) are allowed"
        )


def assert_single_text_unit(value: str) -> None:
    """
    Ensure that the input string contains exactly one textual unit.

    A 'text unit' is defined as a single contiguous sequence of non-space characters (word, code,
    identifier, or slug)
    """
    if len(value.split()) != 1:
        raise ValueError("Must consist of exactly 1 (one) text unit (no spaces)")


def assert_valid_word_boundaries(text: str) -> None:
    if any(patterns.INVALID_WORD_BOUNDARIES.search(word) for word in text.split()):
        raise ValueError("Words must start and end with a letter")


def assert_text_starts_with_capital_letter(text: str) -> None:
    first_word = text.split()[0]

    if first_word[0].isalpha() and not first_word[0].isupper():
        raise ValueError("Must start with a capital letter")


def assert_all_letters_are_ukrainian(text: str) -> None:
    letters = patterns.UNICODE_LETTERS.findall(text)  # Only letter characters

    for letter in letters:
        if letter not in patterns.UKRAINIAN_ALPHABET:
            raise ValueError(f"Non-Ukrainian letters detected")


def assert_telegram_handle_is_valid(value: str) -> None:
    """Assert that a string is a valid Telegram handle (without the '@' prefix)."""
    if not (5 <= len(value) <= 32):
        raise ValueError("Telegram handle must be 5-32 characters long")

    if not patterns.TELEGRAM_HANDLE.fullmatch(value):
        raise ValueError(
            "Telegram handle contains invalid characters. Only letters, numbers and underscores "
            "(_) are allowed"
        )


def assert_linkedin_profile_slug_is_valid(value: str) -> None:
    """Assert that a string is a valid LinkedIn profile slug."""
    if not (3 <= len(value) <= 100):
        raise ValueError("LinkedIn user profile slug (custom URL) must be 3-100 characters long")

    if not patterns.LINKEDIN_PROFILE_SLUG.fullmatch(value):
        raise ValueError(
            "LinkedIn user profile slug (custom URL) contains invalid characters. Only lowercase "
            "letters (a-z), numbers (0-9), hyphens (-) and underscores (_) are allowed"
        )


def assert_full_address_is_valid(value: str) -> None:
    """Assert that a string is a valid address."""
    if not (5 <= len(value) <= 255):
        raise ValueError("Address value must be 5-255 characters long")

    if not patterns.ADDRESS.fullmatch(value):
        raise ValueError(
            "Address value contains invalid characters. Only letters, digits (0–9), spaces, commas "
            "(,), periods (.), hyphens (-), and apostrophes (') are allowed"
        )


def assert_postal_code_is_valid(value: str) -> None:
    """Assert that a string is a valid postal code."""
    if not (3 <= len(value) <= 10):
        raise ValueError("Postal code must be 3-10 characters long")

    if not patterns.POSTAL_CODE.fullmatch(value):
        raise ValueError(
            "Postal code contains invalid characters. Only letters (A-Z), digits (0–9), and "
            "hyphens (-) are allowed"
        )
