import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, ReferenceEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.specification import Specification
    from apps.soil_laboratory.models.test_result import TestResult


class Parameter(BaseORM, ReferenceEntityMetadataMixin):
    """SQLAlchemy ORM model for Parameter."""
    __tablename__ = "parameters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    units: Mapped[str | None] = mapped_column(String(120))

    specifications: Mapped[list["Specification"]] = safe_relationship(back_populates="parameter")
    test_results: Mapped[list["TestResult"]] = safe_relationship(back_populates="parameter")

    def __repr__(self) -> str:
        return f"<Parameter id={self.id} name={self.name} units={self.units}>"
