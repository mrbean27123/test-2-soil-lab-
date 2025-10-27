import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, BusinessEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.material import Material
    from apps.soil_laboratory.models.material_source import MaterialSource
    from apps.soil_laboratory.models.test_result import TestResult


class Sample(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for Sample."""
    __tablename__ = "samples"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id", ondelete="CASCADE"),
        nullable=False
    )
    material_source_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("material_sources.id", ondelete="CASCADE"),
        nullable=False
    )

    temperature: Mapped[float] = mapped_column(Float)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    note: Mapped[str | None] = mapped_column(String(1000))

    material: Mapped["Material"] = safe_relationship(back_populates="samples")
    material_source: Mapped["MaterialSource"] = safe_relationship(back_populates="samples")
    test_results: Mapped[list["TestResult"]] = safe_relationship(back_populates="sample")

    def __repr__(self) -> str:
        return (
            f"<Sample id={self.id} material_id={self.material_id} "
            f"material_source_id={self.material_source_id} temperature={self.temperature} "
            f"received_at={self.received_at}>"
        )
