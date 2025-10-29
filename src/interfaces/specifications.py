from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import Select


class SpecificationInterface(ABC):
    """Base interface for specifications."""

    @abstractmethod
    def apply(self, stmt: Select[Any]) -> Select[Any]:
        """Modify and return a new SQLAlchemy Select statement."""
        ...


class PaginationSpecificationInterface(SpecificationInterface):
    """Interface for pagination specifications."""

    @property
    @abstractmethod
    def limit(self) -> int:
        ...

    @property
    @abstractmethod
    def offset(self) -> int:
        ...


class OrderingSpecificationInterface(SpecificationInterface):
    """Interface for query specification that applies ordering."""

    @property
    @abstractmethod
    def ordering_fields(self) -> list[str]:
        """Get list of ordering fields."""
        ...


class FilterSpecificationInterface(SpecificationInterface):
    """Interface for query specification that applies filters."""

    @property
    @abstractmethod
    def is_applicable(self) -> bool:
        """Check if filter specification has any filters."""
        ...
