import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.identity.models.relationships import roles_permissions, users_roles
from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.identity.models import Permission, User


class Role(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for Role."""
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    permissions: Mapped[list["Permission"]] = safe_relationship(
        secondary=roles_permissions,
        back_populates="roles"
    )
    users: Mapped[list["User"]] = safe_relationship(secondary=users_roles, back_populates="roles")

    def __repr__(self):
        return f"<Role id={self.id} name='{self.name}'>"
