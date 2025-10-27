import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseORM, BusinessEntityMetadataMixin
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.soil_laboratory.models.measurement import Measurement
    from apps.soil_laboratory.models.parameter import Parameter
    from apps.soil_laboratory.models.sample import Sample
    from apps.soil_laboratory.models.specification import Specification


class TestResult(BaseORM, BusinessEntityMetadataMixin):
    """SQLAlchemy ORM model for TestResult."""
    __tablename__ = "test_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    sample_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("samples.id", ondelete="CASCADE"),
        nullable=False
    )
    parameter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("parameters.id", ondelete="RESTRICT"),
        nullable=False
    )

    mean_value: Mapped[float | None] = mapped_column(Float)
    variation_percentage: Mapped[float | None] = mapped_column(Float)

    lower_limit: Mapped[float | None] = mapped_column(Float)
    upper_limit: Mapped[float | None] = mapped_column(Float)

    is_compliant: Mapped[bool] = mapped_column(Boolean)

    sample: Mapped["Sample"] = safe_relationship(back_populates="test_results")
    parameter: Mapped["Parameter"] = safe_relationship(back_populates="test_results")
    # specification: Mapped["Specification"] = safe_relationship(
    #     primaryjoin="""and_(
    #         foreign(TestResult.parameter_id) == Specification.parameter_id,
    #         foreign(Sample.material_id) == Specification.material_id,
    #         foreign(Sample.material_source_id) == Specification.material_source_id,
    #     )""",
    #     uselist=False,
    #     viewonly=True
    # )
    measurements: Mapped[list["Measurement"]] = safe_relationship(back_populates="test_result")

    def __repr__(self) -> str:
        return (
            f"<TestResult id={self.id} sample_id={self.sample_id} parameter_id={self.parameter_id} "
            f"mean_value={self.mean_value} variation_percentage={self.variation_percentage} "
            f"is_compliant={self.is_compliant}>"
        )
