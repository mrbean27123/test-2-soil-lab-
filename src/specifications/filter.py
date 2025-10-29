from dataclasses import dataclass
from typing import Any

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy.orm import InstrumentedAttribute

from interfaces.specifications import FilterSpecificationInterface


class FilteringSpecificationBase(FilterSpecificationInterface):
    """Generic specification for applying validated filtering to SQLAlchemy queries."""

    @dataclass
    class _Filter:
        column_attribute: InstrumentedAttribute
        operator: str
        value: list[Any] | Any
        join_path: InstrumentedAttribute | None = None

    def __init__(self, filters: list[_Filter] | None = None):
        self._filters = filters or []
        self._filter_clauses = self._build_clauses(self._filters)

    @property
    def is_applicable(self) -> bool:
        return True if self._filter_clauses else False

    def apply(self, stmt: Select[Any]) -> Select[Any]:
        """Apply built filter clauses to SQLAlchemy Select."""
        if self.is_applicable:
            for filter_ in self._filters:
                if filter_.join_path:
                    stmt = stmt.join(filter_.join_path)

            stmt = stmt.where(and_(*self._filter_clauses))

        return stmt

    def _build_clauses(self, filters: list[_Filter]) -> list[BinaryExpression]:
        clauses: list[BinaryExpression] = []

        for filter_ in filters:
            if not filter_.value:
                continue

            filter_values = (
                [filter_.value]
                if not isinstance(filter_.value, list)
                else filter_.value
            )

            for value in filter_values:
                clause = self._build_clause(filter_.column_attribute, filter_.operator, value)

                if clause is not None:
                    clauses.append(clause)

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
