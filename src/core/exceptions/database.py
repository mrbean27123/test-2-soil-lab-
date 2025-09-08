from typing import Any
from uuid import UUID

from core.exceptions.base import ServerError


class DatabaseError(ServerError):
    status_code = 500
    default_message = "Database operation failed"


class EntityNotFoundError(DatabaseError):
    status_code = 404
    default_message = "Entity not found"

    def __init__(
        self,
        entity_class: type | None = None,
        entity_id: int | UUID | None = None,
        message: str | None = None,
        details: dict[str, Any] | None = None
    ):
        if entity_class and entity_id and not message:
            details = details or {}

            entity_name = entity_class.__name__
            details["entity_name"] = entity_name
            details["entity_id"] = str(entity_id)

            message = f"Entity <{entity_name}> with id '{entity_id}' not found"

        super().__init__(message, details)


class RelatedEntityNotFoundError(DatabaseError):
    """Raise when related entity for provided ID is not found."""
    status_code = 422
    default_message = "Related entity not found"

    def __init__(
        self,
        entity_name: str,
        missing_id: int | UUID,
        message: str | None = None,
        details: dict[str, Any] | None = None
    ):
        if not message:
            details = details or {}
            details["entity_name"] = entity_name.title()
            details["missing_id"] = missing_id
            message = f"{entity_name.title()} with the following ID not found: {missing_id}"

        super().__init__(message, details)


class RelatedEntitiesNotFoundError(DatabaseError):
    """Raise when related entities for provided IDs are not found."""
    status_code = 422
    default_message = "Related entities not found"

    def __init__(
        self,
        entity_name: str,
        missing_ids: set[int | UUID],
        message: str | None = None,
        details: dict[str, Any] | None = None
    ):
        if not message:
            details = details or {}
            details["entity_name"] = entity_name.title()
            details["missing_ids"] = list(missing_ids)
            message = f"{entity_name.title()} with the following IDs not found: {list(missing_ids)}"

        super().__init__(message, details)
