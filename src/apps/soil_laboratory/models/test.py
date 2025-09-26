import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.soil_laboratory.enums import TestStatus, TestType
from database.models import BaseORM, BusinessEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.sample import Sample


class Test(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for Test."""
    __tablename__ = "tests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    sample_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("samples.id", ondelete="CASCADE"),
        nullable=False
    )

    type_: Mapped[TestType] = mapped_column(
        "type",
        Enum(TestType, values_callable=lambda enum_cls: [e.value for e in enum_cls])
    )

    measurement_1: Mapped[float] = mapped_column(Float)
    measurement_2: Mapped[float] = mapped_column(Float)
    measurement_3: Mapped[float | None] = mapped_column(Float)

    selected_measurement_1: Mapped[float] = mapped_column(Float)
    selected_measurement_2: Mapped[float] = mapped_column(Float)

    difference_percent: Mapped[float] = mapped_column(Float)
    mean_measurement: Mapped[float] = mapped_column(Float)

    lower_limit: Mapped[float] = mapped_column(Float)
    upper_limit: Mapped[float] = mapped_column(Float)

    status: Mapped[TestStatus] = mapped_column(
        "status",
        Enum(TestStatus, values_callable=lambda enum_cls: [e.value for e in enum_cls])
    )

    sample: Mapped["Sample"] = safe_relationship(back_populates="tests")

    def __repr__(self) -> str:
        return f"<Test id={self.id} type={self.type_} mean_measurement={self.mean_measurement}>"
