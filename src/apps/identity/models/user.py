import uuid
from datetime import datetime
from typing import Self, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.identity.models.relationships import users_permissions, users_roles
from core.security.passwords import hash_password, verify_password
from database.models import BaseORM, BusinessEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.identity.models import Permission, RefreshToken, Role


class User(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for User."""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(String(255), unique=True)
    _hashed_password: Mapped[str] = mapped_column("hashed_password", String(255))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    roles: Mapped[list["Role"]] = safe_relationship(secondary=users_roles, back_populates="users")
    permissions: Mapped[list["Permission"]] = safe_relationship(
        secondary=users_permissions,
        back_populates="users"
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = safe_relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        raw_password: str,
        is_active: bool = True,
        is_superuser: bool = False
    ) -> Self:
        """
        Factory method to create a new User instance.

        This method simplifies the creation of a new user by handling password hashing and setting
        required attributes.
        """
        user = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            is_superuser=is_superuser
        )
        user.password = raw_password

        return user

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only. Use the setter to set the password.")

    @password.setter
    def password(self, raw_password: str) -> None:
        """Set the user's password after validating its strength and hashing it."""
        # validators.validate_password_strength(raw_password)
        self._hashed_password = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """Verify the provided password against the stored hashed password."""
        return verify_password(raw_password, self._hashed_password)

    def __repr__(self) -> str:
        return f"<User id={self.id} email='{self.email}')>"
