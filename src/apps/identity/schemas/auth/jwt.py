from pydantic import BaseModel, ConfigDict, EmailStr, Field


class JWTSchemaBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class LoginRequest(JWTSchemaBase):
    email: EmailStr
    password: str


class LogoutRequest(JWTSchemaBase):
    refresh_token: str = Field(alias="refreshToken")


class TokenRefreshRequest(JWTSchemaBase):
    refresh_token: str = Field(alias="refreshToken")


class TokenRefreshResponse(JWTSchemaBase):
    access_token: str = Field(alias="accessToken")
    token_type: str = Field("bearer", alias="tokenType")


class TokenPairResponse(JWTSchemaBase):
    access_token: str = Field(alias="accessToken")
    refresh_token: str | None = Field(None, alias="refreshToken")
    token_type: str = Field("bearer", alias="tokenType")
