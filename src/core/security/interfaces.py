from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class JWTManagerInterface(ABC):
    """Interface for JWT token management operations."""

    @abstractmethod
    def create_access_token(self, data: dict[str, Any]) -> str:
        """Create a new access token."""
        ...

    @abstractmethod
    def create_refresh_token(self, data: dict[str, Any]) -> str:
        """Create a new refresh token."""
        ...

    @abstractmethod
    def decode_access_token(self, token: str) -> dict[str, Any]:
        """Verify and decode an access token."""
        ...

    @abstractmethod
    def decode_refresh_token(self, token: str) -> dict[str, Any]:
        """Verify and decode a refresh token."""
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> None:
        """Verify an access token and raise an error if it's invalid or expired."""
        ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> None:
        """Verify a refresh token and raise an error if it's invalid or expired."""
        ...

    @abstractmethod
    def get_token_expiration(self, token: str) -> datetime:
        """Get the expiration time of a token."""
        ...
