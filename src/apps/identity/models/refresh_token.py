import uuid
from datetime import datetime, timedelta, timezone
from typing import Self, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from apps.identity.models.token_base import BaseToken
from core.security.utils import generate_secure_token
from database.utils import safe_relationship


if TYPE_CHECKING:
    from apps.identity.models import User


class RefreshToken(BaseToken):
    """SQLAlchemy ORM model for RefreshToken."""
    __tablename__ = "refresh_tokens"

    TOKEN_LENGTH = 512

    token: Mapped[str] = mapped_column(
        String(TOKEN_LENGTH),
        unique=True,
        default=generate_secure_token
    )

    user: Mapped["User"] = safe_relationship(back_populates="refresh_tokens", uselist=False)

    @classmethod
    def create(cls, user_id: uuid.UUID, days_valid: int, token: str | None = None) -> Self:
        """
        Factory method to create a new RefreshToken instance.

        This method simplifies the creation of a new refresh token by calculating the expiration
        date based on the provided number of valid days and setting the required attributes.
        """
        expires_at = datetime.now(timezone.utc) + timedelta(days=days_valid)
        token_value = token or generate_secure_token()

        return cls(user_id=user_id, expires_at=expires_at, token=token_value)

    def __repr__(self):
        return (
            f"<RefreshToken id={self.id}, user_id={self.user_id}, expires_at={self.expires_at}, "
            f"token={self.token[:8]}...)>"
        )
