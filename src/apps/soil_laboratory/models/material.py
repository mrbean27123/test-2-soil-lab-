import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.material_type import MaterialType
    from apps.soil_laboratory.models.sample import Sample
    from apps.soil_laboratory.models.specification import Specification


class Material(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for Material."""
    __tablename__ = "materials"
    __table_args__ = (
        UniqueConstraint("material_type_id", "name", name="uq_material_type_id_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    material_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("material_types.id", ondelete="RESTRICT"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(120))

    material_type: Mapped["MaterialType"] = safe_relationship(back_populates="materials")
    samples: Mapped[list["Sample"]] = safe_relationship(back_populates="material")
    specifications: Mapped[list["Specification"]] = safe_relationship(back_populates="material")

    def __repr__(self) -> str:
        return f"<Material id={self.id} material_type_id={self.material_type_id} name={self.name}>"
