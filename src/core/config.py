from pathlib import Path
from typing import Final, Literal
from uuid import UUID

from pydantic import EmailStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Root directory for resolving the paths
ROOT_DIR = Path(__file__).resolve().parents[2]  # app-soil-lab/

ENV_PATH = ROOT_DIR / ".env"
BASE_DIR = ROOT_DIR / "src/"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )

    # Application
    ENVIRONMENT: Literal["local", "testing", "staging", "production"] = "local"
    APP_NAME: str = "soil_laboratory"

    BASE_DIR: Path = BASE_DIR

    # JWT / Security
    JWT_SECRET_KEY_ACCESS: str
    JWT_SECRET_KEY_REFRESH: str
    JWT_ALGORITHM: str = "HS256"

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # PostgreSQL
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # noinspection PyPep8Naming
    @computed_field
    @property
    def ASYNC_POSTGRES_DATABASE_URL(self) -> str:
        """Data Source Name for async PostgreSQL connection."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # noinspection PyPep8Naming
    @computed_field
    @property
    def SYNC_POSTGRES_DATABASE_URL(self) -> str:
        """Data Source Name for sync PostgreSQL connection (e.g., for Alembic)."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # pgAdmin
    # PGADMIN_DEFAULT_EMAIL: str
    # PGADMIN_DEFAULT_PASSWORD: str

    # First superuser data
    SYSTEM_USER_ID: UUID
    SYSTEM_USER_EMAIL: EmailStr
    SYSTEM_USER_PASSWORD: str

    # Logging
    LOG_LEVEL: str = "info"

    # Testing
    PATH_TO_TESTING_DB: str = ":memory:"


# Global settings instance
settings: Final[Settings] = Settings()
