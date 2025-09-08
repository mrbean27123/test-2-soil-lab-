import uuid

from sqlalchemy import Float, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, BusinessEntityMetadataMixin


class Measurement(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for Measurement."""
    __tablename__ = "measurements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    molding_sand_number: Mapped[str] = mapped_column(String(50))

    molding_sand_strength_kgf_cm2: Mapped[float] = mapped_column(Float)
    molding_sand_gas_permeability: Mapped[float] = mapped_column(Float)
    molding_sand_moisture_percent: Mapped[float] = mapped_column(Float)

    note: Mapped[str | None] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return (
            f"<Measurement id={self.id} "
            f"molding_sand_strength_kgf_cm2='{self.molding_sand_strength_kgf_cm2}' "
            f"molding_sand_gas_permeability='{self.molding_sand_strength_kgf_cm2}' "
            f"molding_sand_moisture_percent='{self.molding_sand_strength_kgf_cm2}'>"
        )
