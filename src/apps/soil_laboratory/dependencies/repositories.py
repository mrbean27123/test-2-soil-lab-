from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.repositories import (
    MaterialRepository,
    MaterialSourceRepository,
    MaterialTypeRepository,
    MeasurementRepository,
    ParameterRepository,
    SampleRepository,
    SpecificationRepository,
    TestResultRepository
)
from database.dependencies import get_postgresql_db_session as get_db_session


def get_material_repository(db: AsyncSession = Depends(get_db_session)) -> MaterialRepository:
    return MaterialRepository(db)


def get_material_source_repository(
    db: AsyncSession = Depends(get_db_session)
) -> MaterialSourceRepository:
    return MaterialSourceRepository(db)


def get_material_type_repository(
    db: AsyncSession = Depends(get_db_session)
) -> MaterialTypeRepository:
    return MaterialTypeRepository(db)


def get_measurement_repository(db: AsyncSession = Depends(get_db_session)) -> MeasurementRepository:
    return MeasurementRepository(db)


def get_parameter_repository(db: AsyncSession = Depends(get_db_session)) -> ParameterRepository:
    return ParameterRepository(db)


def get_sample_repository(db: AsyncSession = Depends(get_db_session)) -> SampleRepository:
    return SampleRepository(db)


def get_specification_repository(
    db: AsyncSession = Depends(get_db_session)
) -> SpecificationRepository:
    return SpecificationRepository(db)


def get_test_result_repository(db: AsyncSession = Depends(get_db_session)) -> TestResultRepository:
    return TestResultRepository(db)
