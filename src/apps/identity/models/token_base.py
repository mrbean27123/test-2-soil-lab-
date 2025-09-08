import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.security.utils import generate_secure_token
from database.models.base import BaseORM


class BaseToken(BaseORM):
    __abstract__ = True

    TOKEN_LENGTH: int = 64

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    token: Mapped[str] = mapped_column(
        String(TOKEN_LENGTH),
        unique=True,
        default=generate_secure_token
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1)
    )

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
