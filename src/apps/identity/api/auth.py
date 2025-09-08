from fastapi import APIRouter, Depends, status

from apps.identity.dependencies.auth import get_auth_service
from apps.identity.schemas import (
    LoginRequest,
    LogoutRequest,
    TokenPairResponse,
    TokenRefreshRequest,
    TokenRefreshResponse
)
from apps.identity.services import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenPairResponse,
    summary="Login User",
    description="Authenticate the user and issue access and refresh tokens to start a new session.",
    status_code=status.HTTP_201_CREATED
)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenPairResponse:
    """
    Authenticate a user and return a new access and refresh token pair.

    - Validate the user's email and password.
    - Issue a new token pair, including an access token for authorization and a refresh token for
    session continuity.
    """
    return await auth_service.get_token_pair(login_data)


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    summary="Refresh Access Token",
    description="Use a refresh token to issue a new access token and maintain the user session.",
    status_code=status.HTTP_200_OK
)
async def refresh_access_token(
    refresh_token_data: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenRefreshResponse:
    """
    Refresh access token using a valid refresh token.

    - Validate and decode the provided refresh token.
    - Ensure token is still valid and tied to a real user.
    - Issue a new access token.
    """
    return await auth_service.refresh_access_token(refresh_token_data)


@router.post(
    "/logout",
    summary="Logout User",
    description="Revoke the refresh token to log the user out and end the current session.",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
    refresh_token_data: LogoutRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Log out the user by invalidating the provided refresh token.

    - Validate and decode the provided refresh token.
    - Verify its integrity and remove it from the database, effectively logging the user out.

    If the token has already been invalidated or not found, the request is silently accepted for
    idempotency.
    """
    return await auth_service.logout(refresh_token_data)
