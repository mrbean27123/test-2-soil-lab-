import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.material import Material


class MaterialType(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for MaterialType."""
    __tablename__ = "material_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    materials: Mapped[list["Material"]] = safe_relationship(back_populates="material_type")

    def __repr__(self) -> str:
        return f"<MaterialType id={self.id} name={self.name}>"
