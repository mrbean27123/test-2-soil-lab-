import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, UUID, event, func
from sqlalchemy.orm import Mapped, mapped_column

from core import context
from core.config import settings


class BasicAuditMixin:
    """Audit mixin: automatic created_at and updated_at timestamps."""
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class AuditMixin:
    """
    Audit mixin: creation and update timestamps with user IDs for each operation.

    User IDs are automatically populated through SQLAlchemy event listeners.
    """
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))


class SoftDeleteMixin:
    """Mixin for soft delete fields."""
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))


class SoftArchiveMixin:
    """Mixin for an 'active/archived' status instead of soft delete (for reference entities)."""
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OptimisticLockingMixin:
    """Mixin for optimistic locking mechanism."""
    version: Mapped[int] = mapped_column(Integer, server_default="1")
    __mapper_args__ = {"version_id_col": version}


class BusinessEntityMetadataMixin(AuditMixin, SoftDeleteMixin, OptimisticLockingMixin):
    """
    Complete metadata for business-critical entities.

    Includes full audit trail, soft delete and optimistic locking mechanisms.
    """
    pass


class ReferenceEntityMetadataMixin(BasicAuditMixin, SoftArchiveMixin):
    """Metadata for reference entities."""
    pass


@event.listens_for(AuditMixin, "before_insert", propagate=True)
def _before_insert_listener(_, __, target: AuditMixin):
    """Event listener: populates audit fields before insert."""
    user = context.get_current_user()

    actor_id = user.id if user else settings.SYSTEM_USER_ID

    target.created_by_id = actor_id
    target.updated_by_id = actor_id


@event.listens_for(AuditMixin, "before_update", propagate=True)
def _before_update_listener(_, __, target: AuditMixin):
    """Event listener: populates audit fields before update."""
    user = context.get_current_user()

    target.updated_by_id = user.id if user else settings.SYSTEM_USER_ID
