import copy
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class UserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    email: EmailStr

    is_active: bool
    is_superuser: bool

    role_codes: list[str] = []
    permission_codes: list[str] = []

    def has_role(self, role: str) -> bool:
        """Check if the user has the specified role"""
        return role in self.role_codes

    def has_any_role(self, *roles: str) -> bool:
        """Check if the user has any of the specified roles"""
        return any(role in self.role_codes for role in roles)

    def has_permission(self, permission: str) -> bool:
        """Check if the user has a specific permission"""
        return permission in self.permission_codes

    def has_permissions(self, *permissions: str) -> bool:
        """Checks if the user has all the specified permissions"""
        return all(self.has_permission(perm) for perm in permissions)

    def has_any_permission(self, *permissions: str) -> bool:
        """Checks if the user has at least one of the specified permissions"""
        return any(self.has_permission(perm) for perm in permissions)

    @model_validator(mode="before")
    @classmethod
    def preprocess_data(cls, data: Any) -> Any:
        from apps.identity.models import User

        if isinstance(data, User):
            data = copy.copy(data)
            setattr(data, "role_codes", [role.code for role in data.roles])
            setattr(data, "permission_codes", [perm.code for perm in data.permissions])

        return data
