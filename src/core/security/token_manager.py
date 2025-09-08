from datetime import datetime, timedelta, timezone
from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWSSignatureError, JWTClaimsError

from core.security.exceptions import (
    EmptyTokenError,
    ExpiredTokenError,
    InvalidTokenError,
    InvalidTokenTypeError,
    TokenCreationError,
    TokenSignatureError,
    TokenVerificationError
)
from core.security.interfaces import JWTManagerInterface


class JWTManager(JWTManagerInterface):
    """A manager for creating, decoding, and verifying JWT access and refresh tokens."""

    def __init__(
        self,
        access_secret_key: str,
        refresh_secret_key: str,
        algorithm: str,
        access_expire_minutes: int,
        refresh_expire_days: int
    ):
        """
        Initialize JWT manager with configuration.

        Args:
            access_secret_key: Secret key for access tokens
            refresh_secret_key: Secret key for refresh tokens
            algorithm: JWT signing algorithm
            access_expire_minutes: Access token expiration time in minutes
            refresh_expire_days: Refresh token expiration time in days
        """
        self._access_secret_key = access_secret_key
        self._refresh_secret_key = refresh_secret_key
        self._algorithm = algorithm
        self._access_expire_minutes = access_expire_minutes
        self._refresh_expire_minutes = 60 * 24 * refresh_expire_days

    def create_access_token(self, data: dict[str, Any]) -> str:
        """Create a new access token."""
        try:
            to_encode = data.copy()
            issued_at = datetime.now(timezone.utc)
            expires_at = issued_at + timedelta(minutes=self._access_expire_minutes)
            to_encode.update({"exp": expires_at, "iat": issued_at, "type": "access"})
        except Exception as e:
            raise TokenCreationError(f"Failed to create access token: {str(e)}", e)

        return jwt.encode(to_encode, self._access_secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        """Create a new refresh token."""
        try:
            to_encode = data.copy()
            issued_at = datetime.now(timezone.utc)
            expires_at = issued_at + timedelta(minutes=self._refresh_expire_minutes)
            to_encode.update({"exp": expires_at, "iat": issued_at, "type": "refresh"})
        except Exception as e:
            raise TokenCreationError(f"Failed to create refresh token: {str(e)}", e)

        return jwt.encode(to_encode, self._refresh_secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict[str, Any]:
        """Verify and decode an access token."""
        if not token or not token.strip():
            raise EmptyTokenError()

        try:
            payload = jwt.decode(token, self._access_secret_key, algorithms=[self._algorithm])

            if payload.get("type") != "access":
                raise InvalidTokenTypeError("Token type must be 'access'")
        except ExpiredSignatureError as e:
            raise ExpiredTokenError("Access token has expired", e)
        except JWSSignatureError as e:
            raise TokenSignatureError("Invalid token signature", e)
        except JWTClaimsError as e:
            raise InvalidTokenError("Invalid token claims", e)
        except JWTError as e:
            raise InvalidTokenError("Invalid token format", e)
        except Exception as e:
            raise TokenVerificationError(f"Failed to verify access token: {str(e)}", e)

        return payload

    def decode_refresh_token(self, token: str) -> dict[str, Any]:
        """Verify and decode a refresh token."""
        if not token or not token.strip():
            raise EmptyTokenError("Token is empty or None")

        try:
            payload = jwt.decode(token, self._refresh_secret_key, algorithms=[self._algorithm])

            if payload.get("type") != "refresh":
                raise InvalidTokenTypeError("Token type must be 'refresh'")
        except ExpiredSignatureError as e:
            raise ExpiredTokenError("Refresh token has expired", e)
        except JWSSignatureError as e:
            raise TokenSignatureError("Invalid token signature", e)
        except JWTClaimsError as e:
            raise InvalidTokenError("Invalid token claims", e)
        except JWTError as e:
            raise InvalidTokenError("Invalid token format", e)
        except Exception as e:
            raise TokenVerificationError(f"Failed to verify refresh token: {str(e)}", e)

        return payload

    def verify_access_token(self, token: str) -> None:
        """Verify an access token and raise an error if it's invalid or expired."""
        self.decode_access_token(token)

    def verify_refresh_token(self, token: str) -> None:
        """Verify a refresh token and raise an error if it's invalid or expired."""
        self.decode_refresh_token(token)

    def get_token_expiration(self, token: str) -> datetime:
        """Get the expiration time of a token."""
        if not token or not token.strip():
            raise EmptyTokenError("Token is empty or None")

        try:
            payload = jwt.get_unverified_claims(token)
            exp_timestamp = payload.get("exp")

            if not exp_timestamp:
                raise TokenVerificationError("Token doesn't contain expiration information")
        except JWTError as e:
            raise InvalidTokenError("Invalid token format", e)
        except Exception as e:
            raise TokenVerificationError(f"Failed to get token expiration: {str(e)}", e)

        return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
