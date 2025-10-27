import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, BusinessEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.test_result import TestResult


class Measurement(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for Measurement."""
    __tablename__ = "measurements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    test_result_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("test_results.id", ondelete="CASCADE"),
        nullable=False
    )

    value: Mapped[float] = mapped_column(Float)

    test_result: Mapped["TestResult"] = safe_relationship(back_populates="measurements")

    def __repr__(self) -> str:
        return f"<Measurement id={self.id} test_result_id={self.test_result_id} value={self.value}>"
