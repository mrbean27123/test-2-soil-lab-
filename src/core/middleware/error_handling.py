import traceback

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from core.exceptions import AppException
from core.logging import AppLoggerInterface


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Centralized error handling middleware.

    Intercepts all exceptions, provides structured error responses, and ensures consistent logging.
    """

    def __init__(self, app: ASGIApp, logger: AppLoggerInterface):
        super().__init__(app)
        self._logger = logger

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response

        except AppException as e:
            # Handle known application exceptions with specific error codes and messages
            self._logger.request_error(e, request)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.message, "exception": traceback.format_exc()},
            )

        except Exception as e:
            # Handle unexpected system exceptions with generic error response
            self._logger.request_unexpected_error(e, request)

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal Server Error. Please contact support.",
                    "exception": traceback.format_exc()
                }
            )
