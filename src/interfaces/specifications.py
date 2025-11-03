from abc import ABC, abstractmethod

from sqlalchemy import Select


class SpecificationInterface(ABC):
    """Interface for a specification that can be applied to a SQLAlchemy query."""

    @abstractmethod
    def apply(self, stmt: Select) -> Select:
        """Applies the specification to a SQLAlchemy Select statement."""
        ...


class PaginationSpecificationInterface(SpecificationInterface):
    """Interface for a pagination specification that can be applied to a query."""

    @property
    @abstractmethod
    def limit(self) -> int:
        """Returns the calculated limit (page size)."""
        ...

    @property
    @abstractmethod
    def offset(self) -> int:
        """Returns the calculated offset (rows to skip)."""
        ...


class OrderingSpecificationInterface(SpecificationInterface):
    """Interface for an ordering specification that can be applied to a query."""

    @property
    @abstractmethod
    def join_paths(self) -> tuple[type, ...]:
        """Returns ORM models required for joins."""
        ...

    @property
    @abstractmethod
    def allowed_fields(self) -> list[str]:
        """Get list of ordering fields."""
        ...

    @property
    @abstractmethod
    def is_applicable(self) -> bool:
        """Check if ordering specification can be applied."""
        ...


class FilterSpecificationInterface(SpecificationInterface):
    """Interface for query specification that applies filters."""

    @property
    @abstractmethod
    def join_paths(self) -> tuple[type, ...]:
        """Get list of join paths."""
        ...

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if filter specification has any filters."""
        ...


class SearchSpecificationInterface(SpecificationInterface):
    """Interface for a search specification that can be applied to a query."""

    @property
    @abstractmethod
    def join_paths(self) -> tuple[type, ...]:
        """Returns ORM models required for joins."""
        ...

    @property
    @abstractmethod
    def query(self) -> str | None:
        """Returns the search query string."""
        ...

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the search specification is empty."""
        ...
