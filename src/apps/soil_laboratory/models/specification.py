import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.material import Material
    from apps.soil_laboratory.models.material_source import MaterialSource
    from apps.soil_laboratory.models.parameter import Parameter


class Specification(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for Specification."""
    __tablename__ = "specifications"
    __table_args__ = (
        UniqueConstraint(
            "parameter_id",
            "material_id",
            "material_source_id",
            name="uq_parameter_id_material_id_material_source_id"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    parameter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("parameters.id", ondelete="CASCADE"),
        nullable=False
    )
    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id", ondelete="CASCADE"),
        nullable=False
    )
    material_source_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("material_sources.id", ondelete="CASCADE"),
        nullable=False
    )

    min_value: Mapped[float | None] = mapped_column(Float)
    max_value: Mapped[float | None] = mapped_column(Float)

    parameter: Mapped["Parameter"] = safe_relationship(back_populates="specifications")
    material: Mapped["Material"] = safe_relationship(back_populates="specifications")
    material_source: Mapped["MaterialSource"] = safe_relationship(back_populates="specifications")

    def __repr__(self) -> str:
        return (
            f"<Specification id={self.id} parameter_id={self.parameter_id} "
            f"material_id={self.material_id} material_source_id={self.material_source_id} "
            f"min_value={self.min_value} max_value={self.max_value}>"
        )
