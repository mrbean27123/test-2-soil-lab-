import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.sample import Sample
    from apps.soil_laboratory.models.specification import Specification


class MaterialSource(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for MaterialSource."""
    __tablename__ = "material_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    samples: Mapped[list["Sample"]] = safe_relationship(back_populates="material_source")
    specifications: Mapped[list["Specification"]] = safe_relationship(
        back_populates="material_source"
    )

    def __repr__(self) -> str:
        return f"<MaterialSource id={self.id} name={self.name}>"
