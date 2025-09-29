from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.repositories.sample import SampleRepository
from apps.soil_laboratory.repositories.test import TestRepository
from apps.soil_laboratory.services.reports.sample_report import SampleReportService
from apps.soil_laboratory.services.sample import SampleService
from apps.soil_laboratory.services.test import TestService
from database.dependencies import get_postgresql_db_session as get_db_session


def get_sample_repository(db: AsyncSession = Depends(get_db_session)) -> SampleRepository:
    return SampleRepository(db)


def get_test_repository(db: AsyncSession = Depends(get_db_session)) -> TestRepository:
    return TestRepository(db)


def get_sample_service(
    db: AsyncSession = Depends(get_db_session),
    sample_repo: SampleRepository = Depends(get_sample_repository)
) -> SampleService:
    return SampleService(db, sample_repo)


def get_sample_report_service(
    sample_repo: SampleRepository = Depends(get_sample_repository)
) -> SampleReportService:
    return SampleReportService(sample_repo)


def get_test_service(
    db: AsyncSession = Depends(get_db_session),
    test_repo: TestRepository = Depends(get_test_repository),
    sample_repo: SampleRepository = Depends(get_sample_repository)
) -> TestService:
    return TestService(db, test_repo, sample_repo)
