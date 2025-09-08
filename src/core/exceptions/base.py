from typing import Any


class AppException(Exception):
    status_code = 500
    default_message = "Internal server error"

    def __init__(self, message: str | None = None, details: dict[str, Any] | None = None):
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class ClientError(AppException):
    status_code = 400
    default_message = "Bad request"


class ServerError(AppException):
    pass
