from typing import Any

from sqlalchemy import Select

from interfaces.specifications import PaginationSpecificationInterface


class PaginationSpecification(PaginationSpecificationInterface):
    def __init__(self, page_number: int, page_size: int):
        if page_size < 0:
            raise ValueError("PaginationSpecification page size cannot be negative")

        if page_number <= 0:
            raise ValueError("PaginationSpecification page number must be positive")

        self._limit = page_size
        self._offset = (page_number - 1) * page_size

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def limit(self) -> int:
        return self._limit

    def apply(self, stmt: Select[Any]) -> Select[Any]:
        return stmt.limit(self._limit).offset(self._offset)
