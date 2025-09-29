from datetime import datetime
from uuid import UUID

from pydantic import Field, computed_field


class SoftArchiveMetadataSchemaMixin:
    archived_at: datetime | None = Field(None, alias="archivedAt")

    @computed_field(alias="isArchived")
    @property
    def is_archived(self) -> bool:
        return self.archived_at is not None


class SoftDeleteMetadataSchemaMixin:
    deleted_at: datetime | None = Field(None, alias="deletedAt")

    @computed_field(alias="isDeleted")
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class ReferenceEntitySchemaMetadataMixin(SoftArchiveMetadataSchemaMixin):
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class BusinessEntitySchemaMetadataMixin(SoftDeleteMetadataSchemaMixin):
    created_at: datetime = Field(alias="createdAt")
    created_by_id: UUID | None = Field(None, alias="createdById")
    updated_at: datetime = Field(alias="updatedAt")
    updated_by_id: UUID | None = Field(None, alias="updatedById")
