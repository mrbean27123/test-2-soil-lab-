from dataclasses import dataclass
from typing import ClassVar

from sqlalchemy import BinaryExpression, ColumnElement, Select, or_
from sqlalchemy.orm import InstrumentedAttribute

from interfaces.specifications import SearchSpecificationInterface


@dataclass(slots=True, frozen=True)
class SearchField:
    """
    Represents a single, configured field for a search specification.

    Attributes:
        name: A logical, human-readable name for the field (e.g., "email").
        orm_attribute: The SQLAlchemy InstrumentedAttribute to query (e.g., User.email).
        operator: The string representation of the ORM method to use (e.g., "ilike", "startswith").
    """
    name: str
    orm_attribute: InstrumentedAttribute
    operator: str


class SearchSpecificationBase(SearchSpecificationInterface):
    """
    Base specification for applying N-field OR-based search to a query.

    This class implements the Specification Pattern. It is designed to be subclassed, not used
    directly. It takes a single search term (`query`) and applies it across multiple pre-configured
    fields (`__search_fields__`) using an `OR` operator.

    Subclasses **must** define the following class attributes:
    Attributes:
        __search_fields__: A tuple of `SearchField` instances defining which columns and operators
        to use for the search.
        __join_paths__: An optional tuple of ORM models required to be joined for the search fields
        to be accessible. (e.g., `(Profile,)` if searching `User.profile.full_name`).
    """
    __search_fields__: ClassVar[tuple[SearchField, ...] | None] = None
    __join_paths__: ClassVar[tuple[type, ...] | None] = None

    def __init_subclass__(cls, **kwargs):
        """
        Validates the subclass configuration at definition time.

        This "class constructor" runs when a subclass (e.g., `UserSearchSpecification`) is defined.
        It enforces that the required class attributes are present, correctly typed, and valid. This
        prevents runtime errors by catching configuration issues early.

        Raises:
            TypeError: If `__search_fields__` is missing, not a tuple, or contains non-SearchField
            objects.
            ValueError: If `__search_fields__` or `__join_paths__` contain duplicate entries.
        """
        super().__init_subclass__(**kwargs)

        # --- 1. Validate '__search_fields__' presence and type ---
        if cls.__search_fields__ is None:
            raise TypeError(f"{cls.__name__} must define the '__search_fields__' class attribute.")

        if not isinstance(cls.__search_fields__, tuple):
            raise TypeError(f"{cls.__name__} error: '__search_fields__' must be a tuple.")

        # --- 2. Validate '__search_fields__' contents ---
        if not all(isinstance(f, SearchField) for f in cls.__search_fields__):
            raise TypeError(
                f"{cls.__name__} error: '__search_fields__' must contain only SearchField "
                f"instances."
            )

        # --- 3. Validate '__search_fields__' uniqueness ---
        if len(set(cls.__search_fields__)) != len(cls.__search_fields__):
            raise ValueError(
                f"{cls.__name__} error: '__search_fields__' must contain unique SearchField "
                f"instances."
            )

        # --- 4. Validate '__join_paths__' uniqueness (if provided) ---
        if cls.__join_paths__ and len(set(cls.__join_paths__)) != len(cls.__join_paths__):
            raise ValueError(
                f"{cls.__name__} error: '__join_paths__' must contain unique ORM model instances."
            )

    def __init__(self, query: str | None):
        """
        Initializes the specification with a search query.

        Args:
            query: The raw search term (e.g., "john doe"). It will be stripped of leading/trailing
            whitespace.
        """
        self._query = query.strip() if query else None
        self._search_clauses = self._build_clauses()

    @property
    def join_paths(self) -> tuple[type, ...] | None:
        """Returns the tuple of ORM models required for joins."""
        return self.__join_paths__

    @property
    def is_empty(self) -> bool:
        """Checks if the search query is empty or was not provided."""
        return not self._query

    @property
    def query(self) -> str | None:
        """Returns the cleaned (stripped) search query."""
        return self._query

    def apply(self, stmt: Select) -> Select:
        """
        Applies the search logic to a SQLAlchemy Select statement.

        If the query is not empty, this method adds a `WHERE` clause that combines all configured
        search field conditions using `OR`.

        Args:
            stmt: The SQLAlchemy `Select` statement to modify.

        Returns:
            The modified `Select` statement with the `WHERE` clause applied.
        """
        if not self.is_empty:
            stmt = stmt.where(or_(*self._search_clauses))

        return stmt

    def _build_clauses(self) -> list[BinaryExpression]:
        """
        Constructs a list of SQLAlchemy binary expressions from the config.

        Iterates over `__search_fields__` and builds a filter condition for each one based on the
        instance's `_query`.

        Returns:
            A list of SQLAlchemy `BinaryExpression` (filter) objects.
        """
        if self.is_empty or not self.__search_fields__:
            return []

        clauses: list[BinaryExpression] = []

        for s_field in self.__search_fields__:
            clause = self._build_clause(s_field.orm_attribute, s_field.operator)

            if clause is not None:
                clauses.append(clause)

        return clauses

    def _build_clause(
        self,
        orm_attr: InstrumentedAttribute,
        operator: str
    ) -> BinaryExpression[bool] | ColumnElement[bool]:
        """
        Builds a single SQLAlchemy expression from an attribute and operator.

        This method maps a declarative string operator (e.g., "ilike") to the corresponding
        SQLAlchemy method (e.g., `column.ilike(...)`).

        Args:
            orm_attr: The SQLAlchemy model attribute (e.g., `User.email`).
            operator: The string operator to apply (e.g., 'startswith').

        Returns:
            The resulting SQLAlchemy `BinaryExpression`.

        Raises:
            ValueError: If the provided `operator` string is not supported in the `match` statement.
        """
        match operator:
            case "like":
                return orm_attr.like(self._query)
            case "ilike":
                return orm_attr.ilike(self._query)
            case "startswith":
                return orm_attr.startswith(self._query)
            case "istartswith":
                return orm_attr.istartswith(self._query)
            case "endswith":
                return orm_attr.endswith(self._query)
            case "iendswith":
                return orm_attr.iendswith(self._query)
            case "contains":
                return orm_attr.contains(self._query)
            case "icontains":
                return orm_attr.icontains(self._query)
            case _:
                raise ValueError(f"Unsupported search operator: {operator}")
