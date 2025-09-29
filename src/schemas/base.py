from typing import Generic, Literal, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InputBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # 🚫 Input validation: forbid unexpected fields
        str_strip_whitespace=True,  # 🧼 String normalization (strip() all strings automatically)

        populate_by_name=True
    )


ModelT = TypeVar("ModelT", bound=InputBase)


class AtomicOperationBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateOperationBase(AtomicOperationBase, Generic[ModelT]):
    """Represents a single atomic 'create' operation within a batch request to create 'ModelT'."""
    action: Literal["create"]
    data: ModelT


class UpdateOperationBase(AtomicOperationBase, Generic[ModelT]):
    """Represents a single atomic 'update' operation within a batch request to modify 'ModelT'."""
    action: Literal["update"]
    data: ModelT
    id: UUID


class DeleteOperationBase(AtomicOperationBase):
    """Represents a single atomic 'delete' operation within a batch request to delete 'ModelT'."""
    action: Literal["delete"]
    id: UUID


ListItemModelT = TypeVar("ListItemModelT")


class PaginatedListResponseBase(BaseModel, Generic[ListItemModelT]):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    data: list[ListItemModelT]
    page: int
    total_pages: int = Field(alias="totalPages")
    total_items: int = Field(alias="totalItems")
