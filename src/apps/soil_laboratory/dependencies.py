from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.repositories.measurement import MeasurementRepository
from apps.soil_laboratory.services.measurement import MeasurementService
from database.dependencies import get_postgresql_db_session as get_db_session


def get_measurement_repository(db: AsyncSession = Depends(get_db_session)) -> MeasurementRepository:
    return MeasurementRepository(db)


def get_measurement_service(
    db: AsyncSession = Depends(get_db_session),
    measurement_repo: MeasurementRepository = Depends(get_measurement_repository)
) -> MeasurementService:
    return MeasurementService(db, measurement_repo)
