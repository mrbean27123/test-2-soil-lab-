from typing import Generic, Literal, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SchemaBase(BaseModel):
    """Base class for all Pydantic schemas in the project."""
    model_config = ConfigDict(
        # 🐍->🐫 Auto-generate camelCase aliases from snake_case field names
        alias_generator=to_camel,

        # 🔄 Allow populating models by either alias or the original field name
        populate_by_name=True
    )


class InputSchemaBase(SchemaBase):
    """Base class for schemas used for input data validation (e.g., in request bodies)."""
    model_config = ConfigDict(
        extra="forbid",  # 🚫 Forbid unexpected fields during input validation
        str_strip_whitespace=True,  # 🧼 String normalization (strip() all strings automatically)
    )


IdentifierT = TypeVar("IdentifierT")


class ResponseSchemaBase(SchemaBase, Generic[IdentifierT]):
    """Base class for schemas used for output data serialization (e.g., in response bodies)."""
    model_config = ConfigDict(
        from_attributes=True,  # 🔄 Enable creating schemas directly from ORM model instances
    )

    id: IdentifierT


InputSchemaModelT = TypeVar("InputSchemaModelT", bound=InputSchemaBase)


class AtomicOperationBase(SchemaBase):
    model_config = ConfigDict(extra="forbid")


class CreateOperationBase(AtomicOperationBase, Generic[InputSchemaModelT]):
    """Represents a single atomic 'create' operation within a batch request to create 'ModelT'."""
    action: Literal["create"]
    data: InputSchemaModelT


class UpdateOperationBase(AtomicOperationBase, Generic[InputSchemaModelT]):
    """Represents a single atomic 'update' operation within a batch request to modify 'ModelT'."""
    action: Literal["update"]
    data: InputSchemaModelT
    id: UUID


class DeleteOperationBase(AtomicOperationBase):
    """Represents a single atomic 'delete' operation within a batch request to delete 'ModelT'."""
    action: Literal["delete"]
    id: UUID


SchemaModelT = TypeVar("SchemaModelT", bound=SchemaBase)


class PaginatedListResponseBase(SchemaBase, Generic[SchemaModelT]):
    model_config = ConfigDict(from_attributes=True)

    data: list[SchemaModelT]
    page: int
    total_pages: int
    total_items: int
