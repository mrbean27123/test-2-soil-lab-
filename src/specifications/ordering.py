from typing import Any, Type

from sqlalchemy import ColumnElement, Select
from sqlalchemy.orm import ColumnProperty, DeclarativeBase, InstrumentedAttribute

from interfaces.specifications import OrderingSpecificationInterface


class OrderingSpecification(OrderingSpecificationInterface):
    """
    Specification for applying validated, dynamic ordering to a SQLAlchemy query.

    This class parses a user-provided ordering string (e.g., "name,-created_at"), validates that
    each field corresponds to a sortable database column (a ColumnProperty), and builds a list of
    SQLAlchemy ColumnElement clauses ("ASC" or "DESC").

    It safely ignores non-column attributes such as relationships or methods. If no valid
    user-provided ordering is found, a default ordering is applied instead.
    """

    def __init__(
        self,
        model: Type[DeclarativeBase],
        default_ordering: str | list[ColumnElement] | None = None,
        ordering: str | None = None
    ):
        """
        Initializes the specification and pre-builds ordering clauses.

        Args:
            model: The SQLAlchemy model class (e.g., User) to sort against.
            default_ordering: Default ordering definition, either as a string (e.g., "name,-email")
            or as a list of SQLAlchemy ColumnElements.
            ordering: A comma-separated string of fields to sort by (e.g., "name,-email").
        """
        self._model = model

        if isinstance(default_ordering, list):
            self._default_ordering_clauses = default_ordering
        elif isinstance(default_ordering, str):
            self._default_ordering_clauses = self._build_ordering_clauses_from_str(default_ordering)
        else:
            self._default_ordering_clauses = []

        self._ordering_clauses = self._build_ordering_clauses_from_str(ordering)

    @property
    def ordering_fields(self) -> list[str]:
        """
        Returns the active ordering clauses (fields) as string representations.

        Returns:
            A list of strings, e.g., ["users.name ASC", "users.created_at DESC"].
        """
        return [str(clause) for clause in self._ordering_clauses]

    def apply(self, stmt: Select[Any]) -> Select[Any]:
        """
        Applies the prepared ordering clauses to a Select statement.

        Args:
            stmt: The SQLAlchemy Select statement to modify.

        Returns:
            The modified Select statement with the .order_by() clause applied.
        """
        if self._ordering_clauses:
            stmt = stmt.order_by(*self._ordering_clauses)

        return stmt

    def _build_ordering_clauses_from_str(self, ordering: str | None) -> list[ColumnElement]:
        """
        Parses the ordering string and builds a list of valid ColumnElements.

        Args:
            ordering: The raw, comma-separated ordering string.

        Returns:
            A list of ColumnElement objects (e.g., [User.name.asc(), User.created_at.desc()]) ready
            for use in .order_by().
        """
        ordering_clauses = []

        if ordering:
            raw_fields = ordering.split(",")

            for field_str in raw_fields:
                clause = self._validate_and_get_clause(field_str)

                if clause is not None:
                    ordering_clauses.append(clause)

        # If no valid ordering was provided, apply the default ordering (if available)
        if not ordering_clauses and self._default_ordering_clauses:
            ordering_clauses.extend(self._default_ordering_clauses)

        return ordering_clauses

    def _validate_and_get_clause(self, field_str: str) -> ColumnElement | None:
        """
        Validates a single field string and converts it to a corresponding ColumnElement.

        Args:
            field_str: A single field string, e.g., "name" or "-created_at".

        Returns:
            The ColumnElement (e.g., User.name.desc()) if valid, otherwise None.
        """
        is_desc = field_str.startswith("-")
        field_name = field_str.lstrip("-")

        if not hasattr(self._model, field_name):
            return None

        attr = getattr(self._model, field_name)

        if (
            not isinstance(attr, InstrumentedAttribute)
            or not isinstance(attr.property, ColumnProperty)
        ):
            return None

        column: InstrumentedAttribute = attr
        clause = column.desc() if is_desc else column.asc()

        return clause
