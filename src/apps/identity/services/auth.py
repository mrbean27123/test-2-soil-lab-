from uuid import UUID

from jose import JWTError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.repositories.token import TokenRepository
from core.config import settings
from apps.identity.exceptions import (
    InvalidCredentialsError,
    TokenCreationError,
    TokenExpiredError,
    TokenValidationError,
    UserNotFoundError
)
from core.security.interfaces import JWTManagerInterface
from apps.identity.models import RefreshToken, User
from apps.identity.repositories.user import UserLoadOptions, UserRepository
from apps.identity.schemas import (
    UserData,
    LoginRequest,
    LogoutRequest,
    TokenPairResponse,
    TokenRefreshRequest,
    TokenRefreshResponse
)


class AuthService:
    def __init__(
        self,
        db: AsyncSession,
        jwt_manager: JWTManagerInterface,
        user_repo: UserRepository,
        token_repo: TokenRepository
    ):
        self.db = db
        self.jwt_manager = jwt_manager
        self.user_repo = user_repo
        self.token_repo = token_repo

        self.redis = None  # TODO: connect Redis
        self.cache_ttl = 900  # == 15 minutes

    async def get_user_data(self, user_id: UUID) -> UserData | None:
        """Retrieve User data from cache or database"""
        # Check Redis cache
        # cache_key = f"user_data:{user_id}"
        # cached = await self.redis.get(cache_key) if self.redis else None
        # if cached:
        #     data = json.loads(cached)
        #     return UserData(**data)

        user = await self.user_repo.get_by_id(
            user_id,
            include=[UserLoadOptions.ROLES, UserLoadOptions.PERMISSIONS]
        )

        if not user:
            return None

        # Cache into Redis
        # if self.redis:
        #     await self.redis.setex(
        #         cache_key,
        #         self.cache_ttl,
        #         user_data.model_dump_json()
        #     )

        return UserData.model_validate(user)

    async def get_token_pair(self, login_data: LoginRequest) -> TokenPairResponse:
        """
        Authenticate a user and return a new access and refresh token pair.

        - Validate the user's email and password.
        - Issue a new token pair, including an access token for authorization and a refresh token
        for session continuity.
        """
        user = await self.user_repo.get_by_email(str(login_data.email))

        if not user:
            raise UserNotFoundError(user_email=login_data.email)

        if not user.verify_password(login_data.password):
            raise InvalidCredentialsError("Invalid password")

        try:
            refresh_token_str = self.jwt_manager.create_refresh_token({"sub": str(user.id)})
            refresh_token = RefreshToken.create(
                user_id=user.id,
                token=refresh_token_str,
                days_valid=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
            )

            await self.token_repo.save_refresh_token(refresh_token)
            await self.db.commit()
        except SQLAlchemyError as e:
            raise TokenCreationError("Failed to create refresh token") from e

        access_token_str = self._create_access_token_with_user_data(user)

        return TokenPairResponse(access_token=access_token_str, refresh_token=refresh_token_str)

    async def refresh_access_token(
        self,
        refresh_token_data: TokenRefreshRequest
    ) -> TokenRefreshResponse:
        refresh_token = refresh_token_data.refresh_token

        try:
            payload = self.jwt_manager.decode_refresh_token(refresh_token)
        except JWTError as error:
            raise TokenValidationError(f"Failed to decode token: {str(error)}")

        user_id = UUID(payload.get("sub"))
        db_refresh_token = await self.token_repo.get_refresh_token_by_token(refresh_token)

        if not db_refresh_token:
            raise TokenValidationError("Refresh token not found")

        if db_refresh_token.is_expired():
            raise TokenExpiredError("Refresh token has expired")

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id=user_id)

        new_access_token = self._create_access_token_with_user_data(user)

        return TokenRefreshResponse(access_token=new_access_token)

    async def logout(self, refresh_token_data: LogoutRequest) -> bool:
        refresh_token = refresh_token_data.refresh_token

        try:
            payload = self.jwt_manager.decode_refresh_token(refresh_token)
        except JWTError as error:
            raise TokenValidationError(f"Failed to decode token: {str(error)}")

        user_id = UUID(payload.get("sub"))
        db_refresh_token = await self.token_repo.get_refresh_token_by_token_and_user_id(
            token=refresh_token,
            user_id=user_id
        )

        if not db_refresh_token:
            # logger.info(f"Logout attempt for user {user_id}, token already invalidated.")
            return False

        await self.token_repo.delete_refresh_token(db_refresh_token)
        await self.db.commit()

        return True

    def _create_access_token_with_user_data(self, user: User) -> str:
        user_data = {"sub": str(user.id), "email": user.email}
        jwt_access_token = self.jwt_manager.create_access_token(user_data)

        return jwt_access_token
