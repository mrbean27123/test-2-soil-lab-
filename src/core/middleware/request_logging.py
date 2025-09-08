import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

import core.context as context
from core.logging import AppLoggerInterface


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging incoming HTTP requests and their processing time."""

    def __init__(self, app: ASGIApp, logger: AppLoggerInterface):
        super().__init__(app)
        self._logger = logger

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get from headers or generate a correlation ID for tracing this request
        correlation_id = request.headers.get("Correlation-Id", str(uuid.uuid4()))
        # Set correlation ID as ContextVar
        context.set_correlation_id(correlation_id)
        # Set request method and path as ContextVar
        context.set_request_method(request.method)
        context.set_request_path(request.url.path)

        start_time = time.perf_counter()

        # Log request start
        self._logger.request_start(request)

        # Process the request
        response = await call_next(request)

        # Measure processing time
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Add debug headers to response
        response.headers["Correlation-Id"] = correlation_id

        # Log request end
        self._logger.request_end(request, response.status_code, duration_ms)

        return response
