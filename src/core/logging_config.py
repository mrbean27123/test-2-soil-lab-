from typing import Final

from core.logging import AppLoggerInterface, StructlogLogger, configure_structlog
from core.config import settings


# Configure StructlogLogger
configure_structlog(log_level=settings.LOG_LEVEL, environment=settings.ENVIRONMENT)

# # Global logger instance
logger: Final[AppLoggerInterface] = StructlogLogger(settings.APP_NAME)
