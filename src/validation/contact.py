import email_validator
import phonenumbers
from pydantic import HttpUrl

from validation.internal.text import (
    assert_linkedin_profile_slug_is_valid,
    assert_telegram_handle_is_valid
)


def validate_email(value: str) -> str:
    try:
        validated_email = email_validator.validate_email(value, check_deliverability=False)
        normalized_email = validated_email.normalized

        return normalized_email
    except email_validator.EmailNotValidError as exc:
        raise ValueError(f"Invalid email address: {exc}")


def validate_phone_number(value: str, region: str | None = "UA") -> str:
    try:
        parsed_number = phonenumbers.parse(value, region)

        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError(f"The provided phone number is not valid")

        formatted_number = phonenumbers.format_number(
            parsed_number,
            phonenumbers.PhoneNumberFormat.E164
        )

        return formatted_number
    except phonenumbers.NumberParseException as exc:
        raise ValueError(f"Invalid phone number format: {exc}")


def validate_telegram(value: str) -> str:
    """
    Validate a Telegram handle (e.g., @username) or URL (e.g., t.me/username) and canonicalize it.
    """
    value = value.strip()

    if value.startswith(("t.me/", "https://t.me/", "http://t.me/")):
        # If the value looks like a URL, attempt to extract the handle from the path
        try:
            # Prepend "https://" if no scheme is present for robust parsing
            url = HttpUrl(value if "://" in value else f"https://{value}")
            path = url.path

            if path is None or path.strip("/") == "":
                raise ValueError("Username is missing")

            handle = path.strip("/")
        except ValueError as exc:
            raise ValueError(f"Invalid Telegram URL format: {exc}")
    elif value.startswith("@"):
        # If it's a handle with an "@", strip the prefix
        handle = value[1:]
    else:
        # Otherwise, assume it's a raw handle without any prefixes
        handle = value

    assert_telegram_handle_is_valid(handle)

    formatted_handle = f"@{handle.lower()}"

    return formatted_handle


def validate_url(value: str) -> str:
    if "://" not in value:
        # If scheme is missing, default to "https"
        value = f"https://{value}"

    try:
        url = HttpUrl(value)
    except ValueError as exc:
        raise ValueError(f"Invalid URL format: {exc}")

    return str(url)


def validate_linkedin_url(value: str) -> str:
    url = HttpUrl(validate_url(value))

    if not (url.host == "linkedin.com" or url.host.endswith(".linkedin.com")):
        raise ValueError("LinkedIn profile URL must be a valid 'linkedin.com' address")

    if not url.path or not url.path.startswith("/in/"):
        raise ValueError(
            "LinkedIn profile URL must point to a user profile (should contain '/in/')"
        )

    profile_slug = url.path.split("/in/")[-1].rstrip("/")

    if not profile_slug:
        raise ValueError("LinkedIn user profile slug (custom URL) cannot be empty")

    assert_linkedin_profile_slug_is_valid(profile_slug)

    normalized_url = f"https://linkedin.com/in/{profile_slug}/"

    return normalized_url
