from core.config import settings
from core.security.interfaces import JWTManagerInterface
from core.security.token_manager import JWTManager


def get_jwt_manager() -> JWTManagerInterface:
    """
    Get JWT manager instance

    Returns:
        JWTManager instance configured with settings
    """
    return JWTManager(
        access_secret_key=settings.JWT_SECRET_KEY_ACCESS,
        refresh_secret_key=settings.JWT_SECRET_KEY_REFRESH,
        algorithm=settings.JWT_ALGORITHM,
        access_expire_minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_expire_days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
