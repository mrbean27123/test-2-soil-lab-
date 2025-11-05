from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from sqlalchemy import ColumnElement, Select
from sqlalchemy.orm import InstrumentedAttribute

from interfaces.specifications import OrderingSpecificationInterface
from specifications.mixins import QueryParamParsingMixin


@dataclass(slots=True, frozen=True)
class OrderingField:
    """
    Represents a single, configured field for an ordering specification.

    Attributes:
        name: The public-facing API name for the field (e.g., "created_at"). This is what will be
        provided in the query parameter.
        orm_attribute: The SQLAlchemy InstrumentedAttribute to order by (e.g., User.created_at).
    """
    name: str
    orm_attribute: InstrumentedAttribute


class OrderingSpecificationBase(OrderingSpecificationInterface, QueryParamParsingMixin):
    """
    Base specification for applying dynamic, validated ordering to a query.

    This class implements the Specification Pattern for `ORDER BY` clauses. It is designed to be
    subclassed, not used directly. It parses a front-end query parameter (e.g., "email,-created_at")
    and converts it into a list of safe SQLAlchemy `order_by` clauses (`.asc()` or `.desc()`).

    It enforces security by only allowing ordering on fields explicitly defined in
    `__ordering_fields__`.

    Subclasses **must** define:
    Attributes:
        __ordering_fields__: A tuple of `OrderingField` instances defining which columns can be used
        for ordering.
        __join_paths__: An optional tuple of ORM models required to be joined for the ordering
        fields to be accessible.
        __default_query_param__: An optional fallback ordering string (e.g., "-created_at") to apply
        if no valid query param is provided.
    """
    __ordering_fields__: ClassVar[tuple[OrderingField, ...] | None] = None
    __join_paths__: ClassVar[tuple[type, ...] | None] = None
    __default_query_param__: ClassVar[str | None] = None

    def __init_subclass__(cls, **kwargs):
        """
        Validates the subclass configuration at definition time.

        This "class constructor" runs when a subclass (e.g., `UserOrderingSpecification`) is
        defined. It enforces that the required class attributes are present, correctly typed, and
        valid. This prevents runtime errors by catching configuration issues early.

        Raises:
            TypeError: If `__ordering_fields__` is missing, not a tuple, or contains
            non-OrderingField objects.
            ValueError: If `__ordering_fields__`, `__join_paths__`, or `__default_query_param__`
            contain invalid or duplicate entries.
        """
        super().__init_subclass__(**kwargs)

        # --- 1. Validate '__ordering_fields__' presence and type ---
        if cls.__ordering_fields__ is None:
            raise (
                TypeError(f"{cls.__name__} must define the '__ordering_fields__' class attribute.")
            )

        if not isinstance(cls.__ordering_fields__, tuple):
            raise TypeError(f"{cls.__name__} error: '__ordering_fields__' must be a tuple.")

        # --- 2. Validate '__ordering_fields__' contents ---
        if not all(isinstance(f, OrderingField) for f in cls.__ordering_fields__):
            raise TypeError(
                f"{cls.__name__} error: '__ordering_fields__' must contain only OrderingField "
                f"instances."
            )

        # --- 3. Validate '__ordering_fields__' uniqueness ---
        # Duplicates indicate a configuration error.
        if len(set(cls.__ordering_fields__)) != len(cls.__ordering_fields__):
            raise ValueError(
                f"{cls.__name__} error: '__ordering_fields__' must contain unique SearchField "
                f"instances."
            )

        # --- 4. Validate '__join_paths__' uniqueness and contents (if provided) ---
        if cls.__join_paths__ is not None:
            if (
                len(cls.__join_paths__) == 0  # Must not be an empty tuple
                or len(set(cls.__join_paths__)) != len(cls.__join_paths__)
                or not all(isinstance(p, type) for p in cls.__join_paths__)
            ):
                raise ValueError(
                    f"{cls.__name__} error: '__join_paths__' must be a non-empty tuple of unique "
                    f"ORM model classes."
                )

        # --- 5. Validate '__default_query_param__' contents (if provided) ---
        if cls.__default_query_param__ is not None:
            if (
                not isinstance(cls.__default_query_param__, str)
                or not cls.__default_query_param__.strip()
            ):
                raise ValueError(
                    f"{cls.__name__} error: '__default_query_param__' must be a valid, non-empty "
                    f"string."
                )

    def __init__(self, query_param: str | None):
        """
        Initializes the specification with a user-provided sort query param.

        Args:
            query_param: The raw query string from the user, e.g., "email,-created_at".
        """
        self._ordering_clauses = self._build_clauses_from_query_param(query_param)

    @property
    def join_paths(self) -> tuple[type, ...]:
        """Returns the tuple of ORM models required for joins."""
        return self.__join_paths__

    @cached_property
    def allowed_fields(self) -> list[str]:
        """Returns a list of public-facing field names allowed for ordering."""
        return [field.name for field in self.__ordering_fields__]

    @property
    def is_applicable(self) -> bool:
        """Checks if any valid ordering clauses were generated."""
        return bool(self._ordering_clauses)

    def apply(self, stmt: Select) -> Select:
        """
        Applies the built `ORDER BY` clauses to a SQLAlchemy Select statement.

        If `is_applicable` is True, this method adds the `ORDER BY` clauses to the query.

        Args:
            stmt: The SQLAlchemy `Select` statement to modify.

        Returns:
            The modified `Select` statement with the `ORDER BY` clause(s) applied.
        """
        if self.is_applicable:
            stmt = stmt.order_by(*self._ordering_clauses)

        return stmt

    def _build_clauses_from_query_param(self, query_param: str | None) -> list[ColumnElement]:
        """
        Parses the raw query param string and builds a list of `ORDER BY` clauses.

        It handles comma-separated values and applies the `__default_query_param__` if the provided
        `query_param` is invalid or empty.

        Args:
            query_param: The raw user-provided query string.

        Returns:
            A list of SQLAlchemy `ColumnElement` (ordering) objects (e.g., [User.name.asc(),
            User.created_at.desc()]).
        """
        if not self.__ordering_fields__:
            return []

        def get_clauses_from_raw_query_param(raw_query_param: str | None) -> list[ColumnElement]:
            """
            Inner helper function to process a raw string.

            This is used for both the user-provided param and the default param.
            """
            query_params = self._extract_list_from_query_param(raw_query_param)

            # Build a list, safely ignoring any invalid/unrecognized params
            return [
                clause
                for p in query_params
                if (clause := self._build_clause(p)) is not None
            ]

        # 1. Try to get clauses from the user-provided query param
        ordering_clauses = get_clauses_from_raw_query_param(query_param)

        # 2. If no valid clauses were found, fall back to the default ordering (if available)
        if not ordering_clauses and self.__default_query_param__:
            ordering_clauses = get_clauses_from_raw_query_param(self.__default_query_param__)

        return ordering_clauses

    def _build_clause(self, query_param: str) -> ColumnElement | None:
        """
        Builds a single ColumnElement (ASC/DESC) from a single query param.

        It parses the optional "-" prefix for descending order and, crucially, validates the field
        name against the `__ordering_fields__` allow-list.

        This validation prevents arbitrary column ordering, which can be a security risk (data
        leakage) or cause performance issues.

        Args:
            query_param: A single, clean query parameter (e.g., "-name" or "email").

        Returns:
            A `ColumnElement` (e.g., `User.name.desc()`) if the field is valid, or `None` if the
            field is not in the allow-list.
        """
        # 1. Check for the descending prefix
        is_desc = query_param.startswith("-")

        # 2. Get the clean field name (e.g., "-name" -> "name")
        field_name = query_param.lstrip("-")

        # 3. Securely check against the allow-list
        for ordering_field in self.__ordering_fields__:
            if field_name == ordering_field.name:
                # Found a match. Return the correct ORM attribute with .desc() or .asc() applied.
                return (
                    ordering_field.orm_attribute.desc()
                    if is_desc else ordering_field.orm_attribute.asc()
                )

        # 4. If no match is found, the param is invalid or not allowed - silently ignore it.
        return None
