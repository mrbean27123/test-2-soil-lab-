from uuid import UUID

from fastapi import Depends, Request

import core.context as context
from apps.identity.dependencies.services import get_auth_service
from apps.identity.exceptions import (
    AuthenticationError,
    InsufficientPermissionsError,
    InsufficientPrivilegesError,
    InsufficientRolesError,
    UserNotFoundError
)
from apps.identity.schemas import UserData
from apps.identity.services import AuthService


async def _get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserData:
    x_user_id = getattr(request.state, "user_id", None)

    if not x_user_id:
        raise AuthenticationError("'X-User-Id' header missing")

    try:
        user_id = UUID(x_user_id)
    except ValueError:
        raise AuthenticationError("Invalid user ID format")

    user_data = await auth_service.get_user_data(user_id)

    if not user_data:
        raise UserNotFoundError(user_id=user_id)

    # if user_data.email != x_user_email:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User data mismatch"
    #     )

    # Store authenticated user data as ContextVar for downstream access (logging, etc.)
    context.set_current_user(user_data)

    return user_data


def require_permission(permissions: str | list[str], fallback_roles: list[str] | None = None):
    """
    Check whether the user has the required permissions for current service (department).

    Args:
        permissions: A permission or a list of permissions (all must be present for the user).
        fallback_roles: Roles that automatically grant access. (any role from the list)
    """
    if isinstance(permissions, str):
        permissions = [permissions, ]

    async def dependency(current_user: UserData = Depends(_get_current_user)) -> UserData:
        if current_user.is_superuser:
            return current_user

        # Check roles
        if fallback_roles and current_user.has_any_role(*fallback_roles):
            return current_user

        if not current_user.has_permissions(*permissions):
            raise InsufficientPermissionsError(permissions)

        return current_user

    return dependency


def require_role(roles: str | list[str]):
    """Check whether the user has the required role (or any role from a list)"""
    if isinstance(roles, str):
        roles = [roles, ]

    async def dependency(current_user: UserData = Depends(_get_current_user)) -> UserData:
        if current_user.is_superuser:
            return current_user

        if not current_user.has_any_role(*roles):
            raise InsufficientRolesError(roles)

        return current_user

    return dependency


def require_superuser():
    """Check whether the user is superuser."""

    async def dependency(current_user: UserData = Depends(_get_current_user)) -> UserData:
        if not current_user.is_superuser:
            raise InsufficientPrivilegesError()

        return current_user

    return dependency


def require_login():
    """Ensure the user is authenticated without performing authorization checks."""
    return _get_current_user
