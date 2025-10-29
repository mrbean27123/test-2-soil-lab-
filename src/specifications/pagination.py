from typing import Any

from sqlalchemy import Select

from interfaces.specifications import PaginationSpecificationInterface


class PaginationSpecification(PaginationSpecificationInterface):
    def __init__(self, page: int, per_page: int):
        if per_page < 0:
            raise ValueError("PaginationSpecification 'per_page' cannot be negative")

        if page <= 0:
            raise ValueError("PaginationSpecification 'page' must be positive")

        self._limit = per_page
        self._offset = (page - 1) * per_page

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def limit(self) -> int:
        return self._limit

    def apply(self, stmt: Select[Any]) -> Select[Any]:
        return stmt.limit(self._limit).offset(self._offset)
