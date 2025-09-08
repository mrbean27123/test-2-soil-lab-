from contextvars import ContextVar
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from apps.identity.schemas import UserData

# Context variable for correlation ID to trace logs through requests
_correlation_id_var: ContextVar[str | None] = ContextVar("correlation_id", default=None)

# Context variable for request path
_request_path_var: ContextVar[str | None] = ContextVar("request_path", default=None)

# Context variable for request method
_request_method_var: ContextVar[str | None] = ContextVar("request_method", default=None)

# Context variable for authenticated user data
_current_user_var: ContextVar[Union["UserData", None]] = (ContextVar("current_user", default=None))


def get_correlation_id() -> str:
    """Get correlation id from context."""
    return _correlation_id_var.get()


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation id to context."""
    _correlation_id_var.set(correlation_id)


def get_request_path() -> str:
    """Get request path from context."""
    return _request_path_var.get()


def set_request_path(request_path: str) -> None:
    """Set request path to context."""
    _request_path_var.set(request_path)


def get_request_method() -> str:
    """Get request method from context."""
    return _request_method_var.get()


def set_request_method(request_method: str) -> None:
    """Set request method to context."""
    _request_method_var.set(request_method)


def get_current_user() -> Union["UserData", None]:
    """Get current authenticated user from context."""
    return _current_user_var.get()


def set_current_user(user_data: "UserData") -> None:
    """Set current authenticated user to context."""
    _current_user_var.set(user_data)
