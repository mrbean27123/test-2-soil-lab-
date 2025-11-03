from sqlalchemy import Select

from interfaces.specifications import PaginationSpecificationInterface


class PaginationSpecification(PaginationSpecificationInterface):
    """
    A specification for applying pagination (LIMIT/OFFSET) to a query.

    This class implements the Specification Pattern, encapsulating the logic required to apply
    pagination to a SQLAlchemy `Select` statement. It converts a user-friendly 1-based page number
    and a page size into the corresponding `LIMIT` and `OFFSET` database values.

    It also provides robust validation to prevent invalid pagination parameters (e.g., negative page
    numbers or sizes).
    """

    def __init__(self, page_number: int, page_size: int):
        """
        Initializes the pagination specification and calculates offset/limit.

        Args:
            page_number: The user-facing page number (1-indexed). Must be a positive integer (>= 1).
            page_size: The number of items to include on a page. Must be a non-negative integer
            (>= 0).

        Raises:
            ValueError: If `page_number` is not positive (<= 0) or if `page_size` is negative (< 0).
        """
        # --- 1. Validate page_size ---
        # A page size of 0 is acceptable; it means "return 0 results."
        # A negative page size is a logical impossibility.
        if page_size < 0:
            raise ValueError(f"{self.__class__.__name__} error: page size cannot be negative.")

        # --- 2. Validate page_number ---
        # Page numbering is 1-indexed (e.g., Page 1, Page 2).
        # A zero or negative page number is invalid in this convention.
        if page_number <= 0:
            raise ValueError(
                f"{self.__class__.__name__} error: page number must be positive (1-indexed)."
            )

        self._limit = page_size
        # The offset for a 1-indexed page is (page_number - 1) * page_size
        self._offset = (page_number - 1) * page_size

    @property
    def limit(self) -> int:
        """Returns the calculated `LIMIT` value (the number of rows to return) for the SQL query."""
        return self._limit

    @property
    def offset(self) -> int:
        """Returns the calculated `OFFSET` value (the number of rows to skip) for the SQL query."""
        return self._offset

    def apply(self, stmt: Select) -> Select:
        """
        Applies the pagination (limit and offset) to the query.

        Args:
            stmt: The SQLAlchemy `Select` statement to modify.

        Returns:
            The modified `Select` statement with the `LIMIT` and `OFFSET` applied.
        """
        return stmt.limit(self._limit).offset(self._offset)
