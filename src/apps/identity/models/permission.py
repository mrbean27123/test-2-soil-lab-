import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.identity.models.relationships import roles_permissions, users_permissions
from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.identity.models import Role, User


class Permission(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for Permission."""
    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(1000))

    roles: Mapped[list["Role"]] = safe_relationship(
        secondary=roles_permissions,
        back_populates="permissions"
    )
    users: Mapped[list["User"]] = safe_relationship(
        secondary=users_permissions,
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission id={self.id} code='{self.code}' name='{self.name}'>"
