from dataclasses import dataclass
from typing import Any

from sqlalchemy import BinaryExpression, Select, and_, or_
from sqlalchemy.orm import InstrumentedAttribute

from interfaces.specifications import FilterSpecificationInterface
from specifications.mixins import QueryParamParsingMixin


class FilteringSpecificationBase(FilterSpecificationInterface, QueryParamParsingMixin):
    """Generic specification for applying validated filtering to SQLAlchemy queries."""

    @dataclass(slots=True)
    class _Filter:
        column_attribute: InstrumentedAttribute
        operator: str
        value: Any | list[Any]

    def __init__(
        self,
        filters: list[_Filter] | None = None,
        join_paths: list[type] | None = None
    ):
        self._filters = filters or []
        self._join_paths = join_paths or []

        self._filter_clauses = self._build_clauses(self._filters)

    @property
    def join_paths(self) -> list[type]:
        """Get list of join paths."""
        return self._join_paths

    @property
    def is_empty(self) -> bool:
        return not self._filter_clauses

    def apply(self, stmt: Select[Any]) -> Select[Any]:
        """Apply built filter clauses to SQLAlchemy Select."""
        if not self.is_empty:
            stmt = stmt.where(and_(*self._filter_clauses))

        return stmt

    def _build_clauses(self, filters: list[_Filter]) -> list[BinaryExpression]:
        """
        Builds SQLAlchemy filter clauses from validated filter specifications.

        Each filter may contain one or multiple values. If multiple values are provided for the same
        filter, they are combined using a logical OR (e.g., `?filter[user_id][eq]=14,7,85` →
        `(User.id == 14 OR User.id == 7 OR User.id == 85)`). All resulting filter clauses are then
        combined with AND at a higher query level.

        Args:
            filters (list[_Filter]): A list of validated filter definitions containing the target
            column attribute, operator, and one or more filter values.

        Returns:
            list[BinaryExpression]: A list of SQLAlchemy binary expressions representing the
            filtering conditions.
        """
        clauses: list[BinaryExpression] = []

        for filter_ in filters:
            filter_values = filter_.value if isinstance(filter_.value, list) else [filter_.value]
            sub_clauses = [
                clause
                for fv in filter_values
                if (
                    (clause := self._build_clause(filter_.column_attribute, filter_.operator, fv))
                    is not None
                )
            ]

            if not sub_clauses:
                continue

            clauses.append(
                # Merge multi-value filter with OR, keeping AND logic between different filters
                or_(*sub_clauses) if len(sub_clauses) > 1 else sub_clauses[0]
            )

        return clauses

    @staticmethod
    def _build_clause(
        attr: InstrumentedAttribute,
        operator: str,
        value: Any
    ) -> BinaryExpression | None:
        """Map operator to SQLAlchemy expression."""
        match operator:
            case "eq":
                return attr == value
            case "ne":
                return attr != value
            case "gt":
                return attr > value
            case "gte":
                return attr >= value
            case "lt":
                return attr < value
            case "lte":
                return attr <= value
            case "in":
                if not isinstance(value, (list, tuple, set)):
                    return None

                return attr.in_(value)
            case "ilike":
                return attr.ilike(value)
            case "like":
                return attr.like(value)
            case _:
                raise ValueError(f"Unsupported filtering operator: {operator}")
