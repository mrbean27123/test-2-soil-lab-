from datetime import datetime
from uuid import UUID

from pydantic import computed_field


class SoftArchiveMetadataSchemaMixin:
    archived_at: datetime | None = None

    @computed_field(alias="isArchived")
    @property
    def is_archived(self) -> bool:
        return self.archived_at is not None


class SoftDeleteMetadataSchemaMixin:
    deleted_at: datetime | None = None

    @computed_field(alias="isDeleted")
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class ReferenceEntitySchemaMetadataMixin(SoftArchiveMetadataSchemaMixin):
    created_at: datetime
    updated_at: datetime


class BusinessEntitySchemaMetadataMixin(SoftDeleteMetadataSchemaMixin):
    created_at: datetime
    created_by_id: UUID | None = None
    updated_at: datetime
    updated_by_id: UUID | None = None
