from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Generic, Protocol, Type, TypeVar, runtime_checkable
from uuid import UUID

from sqlalchemy import BinaryExpression, BooleanClauseList, Select, and_, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, Load

from core import context
from core.config import settings
from database.models import BaseORM
from dto import CreateDTOBase, UpdateDTOBase


ModelT = TypeVar("ModelT", bound=BaseORM)
LoadOptionsT = TypeVar("LoadOptionsT", bound=Enum)


@runtime_checkable
class IsBaseRepository(Protocol[ModelT]):
    db: AsyncSession
    model: Type[ModelT]
    _LOAD_OPTIONS_MAP: dict[Enum, Load]

    async def get_by_id(
        self,
        obj_id: UUID,
        include: list[LoadOptionsT] | None = None
    ) -> ModelT | None:
        pass

    def _apply_load_options(
        self,
        stmt: Select,
        include: list[LoadOptionsT] | None = None
    ) -> Select:
        pass


@dataclass(frozen=True)
class PaginationCriteria:
    """Pagination criteria for pagination."""
    limit: int
    offset: int = 0

    def __post_init__(self):
        if self.limit <= 0:
            raise ValueError("PaginationCriteria 'limit' must be positive")
        if self.offset < 0:
            raise ValueError("PaginationCriteria 'offset' cannot be negative")


@dataclass(frozen=True)
class SearchCriteria:
    """Search criteria for text-based filtering."""
    query: str | None
    field: InstrumentedAttribute
    min_query_length: int | None = None
    is_case_sensitive: bool = False

    def __post_init__(self):
        if (self.min_query_length is not None) and not (1 <= self.min_query_length <= 7):
            raise ValueError("SearchCriteria 'min_query_length' must be in range 1-7")

        if self.query is not None:
            normalized_query = self.query.strip()

            if not normalized_query:
                object.__setattr__(self, "query", None)
                return

            if self.min_query_length is not None and len(normalized_query) < self.min_query_length:
                object.__setattr__(self, "query", None)
                return

            if not self.is_case_sensitive:
                normalized_query = normalized_query.lower()

            object.__setattr__(self, "query", normalized_query)

    @property
    def is_applicable(self) -> bool:
        """Check if search criteria should be applied."""
        return self.query is not None


@dataclass(frozen=True)
class OrderCriteria:
    """Ordering criteria for query results."""
    field: InstrumentedAttribute
    ascending: bool = True


class BaseRepository(Generic[ModelT, LoadOptionsT]):
    _LOAD_OPTIONS_MAP: dict[LoadOptionsT, Load] = {}

    def __init__(self, db: AsyncSession, model: Type[ModelT]):
        self.db = db
        self.model = model

    def _apply_load_options(
        self,
        stmt: Select,
        include: list[LoadOptionsT] | None = None
    ) -> Select:
        """Apply SQLAlchemy load options (e.g. joinedload, selectinload) to the statement."""
        if not include or not self._LOAD_OPTIONS_MAP:
            return stmt

        options = [self._LOAD_OPTIONS_MAP[option] for option in include]
        stmt = stmt.options(*options)

        return stmt


class ExistsMixin(Generic[ModelT]):
    async def exists_by_id(self: IsBaseRepository[ModelT], obj_id: UUID) -> bool:
        model_id_field: InstrumentedAttribute = self.model.id

        stmt = select(exists().where(model_id_field == obj_id))
        result = await self.db.execute(stmt)

        return result.scalar()

    async def exists_where(
        self: IsBaseRepository[ModelT],
        *conditions: BinaryExpression | BooleanClauseList
    ) -> bool:
        """
        Check if any record exists matching the given conditions.

        Args:
            *conditions: SQLAlchemy conditions for WHERE clause

        Example:
            # Check if User exists with specific ID
            exists = await repo.exists_where(User.id == user_id)

            # Check if User exists with specific email and is active
            exists = await repo.exists_where(
                User.email == "test@example.com",
                User.is_active == True
            )

            # Check uniqueness during update (exclude current record)
            exists = await repo.exists_where(
                User.email == "new@example.com",
                User.id != current_user_id
            )
        """
        stmt = select(exists().where(and_(*conditions)))
        result = await self.db.execute(stmt)

        return result.scalar()


class CountMixin(Generic[ModelT]):
    async def get_count(
        self: IsBaseRepository[ModelT],
        where_conditions: list[BinaryExpression | BooleanClauseList] | None = None
    ) -> int:
        stmt = select(func.count(self.model.id)).where(and_(*where_conditions))
        result = await self.db.execute(stmt)

        return result.scalar_one()


class LookupMixin(Generic[ModelT]):
    async def get_for_lookup(
        self: IsBaseRepository[ModelT],
        pagination: PaginationCriteria,
        where_conditions: list[BinaryExpression | BooleanClauseList] | None = None,
        search: SearchCriteria | None = None,
        order: OrderCriteria | None = None,
        include: list[LoadOptionsT] | None = None
    ) -> list[ModelT]:
        stmt = select(self.model)

        if where_conditions:
            stmt = stmt.where(and_(*where_conditions))

        # TODO: move it inside SearchCriteria -> stmt = SearchCriteria.apply(stmt)
        if search and search.is_applicable:
            search_pattern = f"%{search.query}%"

            if search.is_case_sensitive:
                stmt = stmt.where(search.field.like(search_pattern))
            else:
                stmt = stmt.where(search.field.ilike(search_pattern))

        stmt = self._apply_load_options(stmt, include)

        # TODO: move it inside OrderCriteria -> stmt = OrderCriteria.apply(stmt)
        if order:
            stmt = stmt.order_by(order.field.asc() if order.ascending else order.field.desc())

        stmt = stmt.offset(pagination.offset).limit(pagination.limit)

        result = await self.db.execute(stmt)

        return list(result.scalars().all())


class ReadPaginatedMixin(Generic[ModelT, LoadOptionsT]):
    """
    Generic pagination mixin for SQLAlchemy-based CRUD repositories.

    This mixin adds a method to fetch paginated results from the database for any model `ModelT`,
    optionally including loader options (`LoadOptionsT`) such as joinedload or selectinload.

    Should be combined with a CRUD base class providing `self.model` and `self.db`.
    """

    async def get_all_paginated(
        self: IsBaseRepository[ModelT],
        pagination: PaginationCriteria,
        where_conditions: list[BinaryExpression | BooleanClauseList] | None = None,
        order: OrderCriteria | None = None,
        include: list[LoadOptionsT] | None = None
    ) -> list[ModelT]:
        """
        Retrieve a paginated list of `ModelT`.

        This method fetches a subset of SQLAlchemy ORM model instances of type `ModelT` from the
        database based on the given pagination parameters.
        """
        stmt = select(self.model)

        if where_conditions:
            stmt = stmt.where(and_(*where_conditions))

        if order:
            stmt = stmt.order_by(order.field.asc() if order.ascending else order.field.desc())

        stmt = self._apply_load_options(stmt, include)
        stmt = stmt.offset(pagination.offset).limit(pagination.limit)
        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def get_all(
        self: IsBaseRepository[ModelT],
        where_conditions: list[BinaryExpression | BooleanClauseList] | None = None,
        order: OrderCriteria | None = None,
        include: list[LoadOptionsT] | None = None
    ) -> list[ModelT]:
        stmt = select(self.model)

        if where_conditions:
            stmt = stmt.where(and_(*where_conditions))

        if order:
            stmt = stmt.order_by(order.field.asc() if order.ascending else order.field.desc())

        stmt = self._apply_load_options(stmt, include)
        result = await self.db.execute(stmt)

        return list(result.scalars().all())


class ReadByIdMixin(Generic[ModelT, LoadOptionsT]):
    async def get_by_id(
        self: IsBaseRepository[ModelT],
        obj_id: UUID,
        include: list[LoadOptionsT] | None = None
    ) -> ModelT | None:
        """Retrieve a single object of `ModelT` by its ID."""
        model_id_field: InstrumentedAttribute = self.model.id

        stmt = select(self.model).where(model_id_field == obj_id)
        stmt = self._apply_load_options(stmt, include)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_many_by_ids(
        self: IsBaseRepository[ModelT],
        obj_ids: list[UUID] | list[int],
        include: list[LoadOptionsT] | None = None
    ) -> list[ModelT]:
        """Retrieve a list of `ModelT` objects by their IDs."""
        model_id_field: InstrumentedAttribute = self.model.id

        stmt = select(self.model).where(model_id_field.in_(obj_ids))
        stmt = self._apply_load_options(stmt, include)
        result = await self.db.execute(stmt)

        return list(result.scalars().all())


class CreateMixin(Generic[ModelT]):
    async def create(self: IsBaseRepository[ModelT], obj_data: CreateDTOBase) -> ModelT:
        obj = self.model(**obj_data.model_dump())
        self.db.add(obj)

        return obj


class UpdateMixin(Generic[ModelT]):
    async def update(
        self: IsBaseRepository[ModelT],
        obj_id: UUID,
        obj_data: UpdateDTOBase
    ) -> ModelT | None:
        db_obj = await self.get_by_id(obj_id)

        if not db_obj:
            return None

        update_data = obj_data.model_dump(exclude_unset=True)

        if not update_data:
            return db_obj

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        return db_obj


class HardDeleteMixin(Generic[ModelT]):
    async def hard_delete(self: IsBaseRepository[ModelT], obj_id: UUID) -> ModelT | None:
        db_obj = await self.get_by_id(obj_id)

        if not db_obj:
            return None

        await self.db.delete(db_obj)

        return db_obj


class SoftDeleteMixin(Generic[ModelT]):
    async def soft_delete(self: IsBaseRepository[ModelT], obj_id: UUID) -> ModelT | None:
        db_obj = await self.get_by_id(obj_id)

        if not db_obj:
            return None

        user = context.get_current_user()
        actor_id = user.id if user else settings.SYSTEM_USER_ID

        setattr(db_obj, "deleted_at", datetime.now(timezone.utc))
        setattr(db_obj, "deleted_by_id", actor_id)

        return db_obj

    async def restore(self: IsBaseRepository[ModelT], obj_id: UUID) -> ModelT | None:
        db_obj = await self.get_by_id(obj_id)

        if not db_obj:
            return None

        setattr(db_obj, "deleted_at", None)
        setattr(db_obj, "deleted_by_id", None)

        return db_obj


class ArchiveByStatusMixin(Generic[ModelT]):
    async def soft_archive(self: IsBaseRepository[ModelT], obj_id: UUID) -> ModelT | None:
        db_obj = await self.get_by_id(obj_id)

        if not db_obj:
            return None

        setattr(db_obj, "archived_at", datetime.now(timezone.utc))

        return db_obj

    async def restore(self: IsBaseRepository[ModelT], obj_id: UUID) -> ModelT | None:
        db_obj = await self.get_by_id(obj_id)

        if not db_obj:
            return None

        setattr(db_obj, "archived_at", None)

        return db_obj
