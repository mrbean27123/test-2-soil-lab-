from dataclasses import dataclass
from typing import Any, Type

from sqlalchemy import BinaryExpression, Select, or_
from sqlalchemy.orm import InstrumentedAttribute

from interfaces.specifications import SearchSpecificationInterface


class SearchSpecificationBase(SearchSpecificationInterface):
    """Generic specification for applying validated filtering to SQLAlchemy queries."""

    @dataclass(slots=True)
    class _SearchField:
        column_attribute: InstrumentedAttribute
        operator: str

    def __init__(
        self,
        query: str,
        search_fields: list[_SearchField] | None = None,
        join_paths: list[Type] | None = None
    ):
        self._query = query
        self._search_fields = search_fields or []
        self._join_paths = join_paths or []

        self._search_clauses = self._build_clauses(self._search_fields)

    @property
    def join_paths(self) -> list[Type]:
        """Get list of join paths."""
        return self._join_paths

    @property
    def is_empty(self) -> bool:
        return not self._query

    @property
    def query(self) -> str:
        return self._query

    def apply(self, stmt: Select[Any]) -> Select[Any]:
        """Apply built search clauses to SQLAlchemy Select."""
        if not self.is_empty:
            stmt = stmt.where(or_(*self._search_clauses))

        return stmt

    def _build_clauses(self, search_fields: list[_SearchField]) -> list[BinaryExpression]:
        if not self._query or not search_fields:
            return []

        clauses: list[BinaryExpression] = []

        for s_field in search_fields:
            clause = self._build_clause(s_field.column_attribute, s_field.operator)

            if clause is not None:
                clauses.append(clause)

        return clauses

    def _build_clause(self, attr: InstrumentedAttribute, operator: str) -> BinaryExpression | None:
        """Map operator to SQLAlchemy expression."""
        match operator:
            case "like":
                return attr.like(self._query)
            case "ilike":
                return attr.ilike(self._query)
            case "startswith":
                return attr.startswith(self._query)
            case "istartswith":
                return attr.istartswith(self._query)
            case "endswith":
                return attr.endswith(self._query)
            case "iendswith":
                return attr.iendswith(self._query)
            case "contains":
                return attr.contains(self._query)
            case "icontains":
                return attr.icontains(self._query)
            case _:
                raise ValueError(f"Unsupported search operator: {operator}")

    @staticmethod
    def _normalize_search_query(value: str | None) -> str | None:
        if not value:
            return None

        value = value.strip()

        return value if value else None
