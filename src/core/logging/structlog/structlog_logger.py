from typing import Any, Literal

import structlog
from fastapi import Request, status

from core.exceptions import AppException
from core.logging.interfaces import AppLoggerInterface


class StructlogLogger(AppLoggerInterface):
    """Structlog application logger."""

    def __init__(self, service_name: str, context: dict[str, Any] | None = None):
        """Initialize the logger, acquiring a pre-configured structlog logger instance."""
        self._logger = structlog.get_logger(service_name)

        if context:
            self._logger = self._logger.bind(**context)

    def log(self, level: int, message: str, **kwargs) -> None:
        self._logger.log(level, message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._logger.error(message, **kwargs)

    def exception(self, message: str, **kwargs) -> None:
        # Automatically adds traceback ("exception" key)
        self._logger.exception(message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        self._logger.critical(message, **kwargs)

    def request_start(self, request: Request, **kwargs) -> None:
        """
        Log the start of request processing.

        Args:
            request: FastAPI Request instance
            **kwargs: Additional data for logging
        """
        log_data = self._extract_request_log_data(request)

        self._logger.info(
            f"Request started: {request.method} {request.url.path}",
            **log_data,
            extra=kwargs
        )

    def request_end(
        self,
        request: Request,
        status_code: int,
        duration_ms: float,
        **kwargs
    ) -> None:
        """
        Log the completion of request processing with performance metrics.

        Args:
            request: FastAPI Request instance
            status_code: HTTP response status code
            duration_ms: Request processing duration in milliseconds
            **kwargs: Additional data for logging
        """
        log_data = self._extract_request_log_data(request)
        log_data.update(
            {
                "status_code": status_code,
                "duration_ms": duration_ms
            }
        )

        self._logger.info(
            f"Request completed: {request.method} {request.url.path} - {status_code} "
            f"({duration_ms:.2f}ms)",
            **log_data,
            extra=kwargs
        )

    def request_error(self, e: AppException, request: Request, **kwargs) -> None:
        log_data = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "error_status_code": e.status_code,
        }
        log_data.update(self._extract_request_log_data(request))

        message = f"Service Error - {e.status_code} - {type(e).__name__}: {e}"

        # Include traceback for server errors (5xx)
        if e.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            self._logger.exception(message, **log_data, extra=kwargs)
        else:
            self._logger.error(message, **log_data, extra=kwargs)

    def request_unexpected_error(self, e: Exception, request: Request, **kwargs) -> None:
        log_data = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "error_status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
        log_data.update(self._extract_request_log_data(request))

        message = (
            f"Unexpected Service Error - {status.HTTP_500_INTERNAL_SERVER_ERROR} - "
            f"{type(e).__name__}: {e}"
        )

        self._logger.exception(message, **log_data, extra=kwargs)

    def entity_action(
        self,
        action: Literal["create", "read", "read_list", "update", "delete", "restore"],
        entity_name: str,
        entity_id: str | None = None,
        **kwargs
    ) -> None:
        log_data = {
            "action": action,
            "entity_name": entity_name,
            "entity_id": entity_id,
        }

        message = f"Entity {action}: {entity_name} id={entity_id}"

        self._logger.info(message, extra=log_data)

    @staticmethod
    def _extract_request_log_data(request: Request) -> dict[str, Any]:
        """Extract logging context from FastAPI Request object."""
        return {
            # "method": request.method,
            # "path": request.url.path,
            "query_params": str(request.query_params) if request.query_params else None,
            "user_agent": str(request.headers.get("User-Agent"))
        }
