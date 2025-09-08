from abc import ABC, abstractmethod
from typing import Literal

from fastapi import Request

from core.exceptions import AppException


class AppLoggerInterface(ABC):
    """App Logger interface."""

    @abstractmethod
    def log(self, level: int, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def exception(self, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def critical(self, message: str, **kwargs) -> None:
        ...

    @abstractmethod
    def request_start(self, request: Request, **kwargs) -> None:
        """
        Log the start of request processing.

        Args:
            request: FastAPI Request instance
            **kwargs: Additional context data for logging
        """
        ...

    @abstractmethod
    def request_end(self, request: Request, status_code: int, duration_ms: float, **kwargs) -> None:
        """
        Log the completion of request processing with performance metrics.
        
        Args:
            request: FastAPI Request instance
            status_code: HTTP response status code
            duration_ms: Request processing duration in milliseconds
            **kwargs: Additional context data for logging
        """
        ...

    @abstractmethod
    def request_error(self, exc: AppException, request: Request, **kwargs) -> None:
        ...

    @abstractmethod
    def request_unexpected_error(self, e: Exception, request: Request, **kwargs) -> None:
        ...

    @abstractmethod
    def entity_action(
        self,
        action: Literal["create", "read", "read_list", "update", "delete", "restore"],
        entity_name: str,
        entity_id: str,
        **kwargs
    ) -> None:
        """
        Log CRUD operations on entities with User context for audit trails.
        
        Args:
            action: Type of operation being performed
            entity_name: Entity being operated on
            entity_id: Entity ID
            **kwargs: Additional context data for logging
        """
        ...
