from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.models import Measurement
from apps.soil_laboratory.repositories.measurement import MeasurementRepository
from apps.soil_laboratory.schemas.measurement import (
    MeasurementCreate,
    MeasurementDetailResponse,
    MeasurementListItemResponse,
    MeasurementListResponse,
    MeasurementLookupResponse,
    MeasurementUpdate
)
from core.exceptions.database import EntityNotFoundError
from core.logging_config import logger
from repositories.base import OrderCriteria, PaginationCriteria, SearchCriteria


class MeasurementService:
    def __init__(self, db: AsyncSession, measurement_repo: MeasurementRepository):
        self.db = db
        self.measurement_repo = measurement_repo

    async def get_measurement_by_id(self, measurement_id: UUID) -> MeasurementDetailResponse:
        measurement = await self.measurement_repo.get_by_id(measurement_id)

        if not measurement:
            raise EntityNotFoundError(Measurement, measurement_id)

        return MeasurementDetailResponse.model_validate(measurement)

    async def get_measurement_lookup_options(
        self,
        limit: int = 100,
        offset: int = 0,
        search: str | None = None
    ) -> list[MeasurementLookupResponse]:
        measurement_entities = await self.measurement_repo.get_for_lookup(
            PaginationCriteria(limit, offset),
            SearchCriteria(search, Measurement.molding_sand_number),
            OrderCriteria(Measurement.created_at)
        )
        response_items = [
            MeasurementLookupResponse.model_validate(measurement)
            for measurement in measurement_entities
        ]

        return response_items

    async def get_measurements_paginated(self, page: int, per_page: int) -> MeasurementListResponse:
        total_measurements = await self.measurement_repo.get_count(
            where_conditions=[Measurement.deleted_at == None, ]
        )
        total_pages = max((total_measurements + per_page - 1) // per_page, 1)
        offset = (page - 1) * per_page

        measurement_entities = await self.measurement_repo.get_all_paginated(
            PaginationCriteria(per_page, offset),
            where_conditions=[Measurement.deleted_at == None, ]
        )
        response_items = [
            MeasurementListItemResponse.model_validate(measurement)
            for measurement in measurement_entities
        ]

        return MeasurementListResponse(
            data=response_items,
            page=page,
            total_pages=total_pages,
            total_items=total_measurements
        )

    async def create_measurement(
        self,
        measurement_data: MeasurementCreate
    ) -> MeasurementDetailResponse:
        measurement = await self.measurement_repo.create(measurement_data.to_dto())

        await self.db.commit()

        return MeasurementDetailResponse.model_validate(measurement)

    async def update_measurement(
        self,
        measurement_id: UUID,
        measurement_data: MeasurementUpdate
    ) -> MeasurementDetailResponse:
        measurement = await self.measurement_repo.update(measurement_id, measurement_data.to_dto())

        if not measurement:
            raise EntityNotFoundError(Measurement, measurement_id)

        await self.db.commit()

        await self.db.refresh(measurement)

        return MeasurementDetailResponse.model_validate(measurement)

    async def delete_measurement(self, measurement_id: UUID) -> MeasurementDetailResponse:
        deleted_measurement = await self.measurement_repo.soft_delete(measurement_id)

        if not deleted_measurement:
            raise EntityNotFoundError(Measurement, measurement_id)

        await self.db.commit()

        await self.db.refresh(deleted_measurement)

        return MeasurementDetailResponse.model_validate(deleted_measurement)

    async def restore_measurement(self, measurement_id: UUID) -> MeasurementDetailResponse:
        restored_measurement = await self.measurement_repo.restore(measurement_id)

        if not restored_measurement:
            raise EntityNotFoundError(Measurement, measurement_id)

        await self.db.commit()

        await self.db.refresh(restored_measurement)

        return MeasurementDetailResponse.model_validate(restored_measurement)
