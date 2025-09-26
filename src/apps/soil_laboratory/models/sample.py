import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, BusinessEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.test import Test


class Sample(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for Sample."""
    __tablename__ = "samples"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    molding_sand_recipe: Mapped[str] = mapped_column(String(50))
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    note: Mapped[str | None] = mapped_column(String(1000))

    tests: Mapped[list["Test"]] = safe_relationship(
        back_populates="sample"
    )

    def __repr__(self) -> str:
        return (
            f"<Sample id={self.id} molding_sand_recipe={self.molding_sand_recipe} "
            f"received_at={self.received_at}>"
        )
