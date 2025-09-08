from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.identity.models import RefreshToken


class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_refresh_token_by_token(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).filter_by(token=token)
        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def get_refresh_token_by_token_and_user_id(
        self,
        token: str,
        user_id: UUID
    ) -> RefreshToken | None:
        stmt = (
            select(RefreshToken)
            .where(RefreshToken.token == token)
            .where(RefreshToken.user_id == user_id)
        )
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def save_refresh_token(self, refresh_token: RefreshToken) -> None:
        self.db.add(refresh_token)

    async def delete_refresh_token(self, refresh_token: RefreshToken) -> None:
        await self.db.delete(refresh_token)
