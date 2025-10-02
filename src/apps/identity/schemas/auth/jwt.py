from pydantic import EmailStr

from schemas.base import SchemaBase


class LoginRequest(SchemaBase):
    email: EmailStr
    password: str


class LogoutRequest(SchemaBase):
    refresh_token: str


class TokenRefreshRequest(SchemaBase):
    refresh_token: str


class TokenRefreshResponse(SchemaBase):
    access_token: str
    token_type: str = "bearer"


class TokenPairResponse(SchemaBase):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
