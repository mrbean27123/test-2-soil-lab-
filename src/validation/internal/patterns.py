import regex


# Pattern to match any Unicode letter character
UNICODE_LETTERS = regex.compile(r"\p{L}", flags=regex.UNICODE)

# Pattern to match characters not allowed in names
# Allows: Latin/Cyrillic letters, spaces, apostrophes ('), hyphens (-)
FORBIDDEN_NAME_CHARACTERS = regex.compile(
    r"[^\p{Latin}\p{Cyrillic}\s'\-]",
    flags=regex.UNICODE
)

SYSTEM_NAME = regex.compile(r"^[a-z]+(?:_[a-z]+)*$")

# Pattern to detect non-letter characters at word boundaries
# (When words don't start/end with Latin or Cyrillic letters)
INVALID_WORD_BOUNDARIES = regex.compile(
    r"(^[^\p{Cyrillic}\p{Latin}])|([^\p{Cyrillic}\p{Latin}]$)",
    flags=regex.UNICODE
)

UKRAINIAN_ALPHABET = set("АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя")

ISO_ALPHA2 = regex.compile(r"^[A-Z]{2}$")
ISO_ALPHA3 = regex.compile(r"^[A-Z]{3}$")
ISO_NUMERIC = regex.compile(r"^\d{3}$")

TELEGRAM_HANDLE = regex.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
LINKEDIN_PROFILE_SLUG = regex.compile(r"^[a-z0-9\-_]+$")

ADDRESS = regex.compile(r"^[\p{L}\p{N}\s\.,'\-]+$", flags=regex.UNICODE)
POSTAL_CODE = regex.compile(r"^[A-Z0-9\- ]{3,10}$", flags=regex.UNICODE)
