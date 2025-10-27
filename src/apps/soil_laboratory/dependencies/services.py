from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.soil_laboratory.dependencies.repositories import (
    get_material_repository,
    get_material_source_repository,
    get_material_type_repository,
    get_measurement_repository,
    get_parameter_repository,
    get_sample_repository,
    get_specification_repository,
    get_test_result_repository
)
from apps.soil_laboratory.repositories import (
    MaterialSourceRepository,
    MaterialTypeRepository,
    MeasurementRepository,
    ParameterRepository,
    SpecificationRepository
)
from apps.soil_laboratory.repositories.material import MaterialRepository
from apps.soil_laboratory.repositories.sample import SampleRepository
from apps.soil_laboratory.repositories.test_result import TestResultRepository
from apps.soil_laboratory.services.material import MaterialService
from apps.soil_laboratory.services.material_source import MaterialSourceService
from apps.soil_laboratory.services.material_type import MaterialTypeService
from apps.soil_laboratory.services.parameter import ParameterService
from apps.soil_laboratory.services.reports.sample_report import SampleReportService
from apps.soil_laboratory.services.sample import SampleService
from apps.soil_laboratory.services.test_result import TestResultService
from database.dependencies import get_postgresql_db_session as get_db_session


def get_material_service(
    db: AsyncSession = Depends(get_db_session),
    material_repo: MaterialRepository = Depends(get_material_repository)
) -> MaterialService:
    return MaterialService(db, material_repo)


def get_material_source_service(
    db: AsyncSession = Depends(get_db_session),
    material_source_repo: MaterialSourceRepository = Depends(get_material_source_repository)
) -> MaterialSourceService:
    return MaterialSourceService(db, material_source_repo)


def get_material_type_service(
    db: AsyncSession = Depends(get_db_session),
    material_type_repo: MaterialTypeRepository = Depends(get_material_type_repository)
) -> MaterialTypeService:
    return MaterialTypeService(db, material_type_repo)


def get_parameter_service(
    db: AsyncSession = Depends(get_db_session),
    parameter_repo: ParameterRepository = Depends(get_parameter_repository)
) -> ParameterService:
    return ParameterService(db, parameter_repo)


def get_sample_service(
    db: AsyncSession = Depends(get_db_session),
    sample_repo: SampleRepository = Depends(get_sample_repository)
) -> SampleService:
    return SampleService(db, sample_repo)


def get_sample_report_service(
    sample_repo: SampleRepository = Depends(get_sample_repository)
) -> SampleReportService:
    return SampleReportService(sample_repo)


def get_test_result_service(
    db: AsyncSession = Depends(get_db_session),
    test_result_repo: TestResultRepository = Depends(get_test_result_repository),
    sample_repo: SampleRepository = Depends(get_sample_repository),
    parameter_repo: ParameterRepository = Depends(get_parameter_repository),
    specification_repo: SpecificationRepository = Depends(get_specification_repository),
    measurement_repo: MeasurementRepository = Depends(get_measurement_repository)
) -> TestResultService:
    return TestResultService(
        db,
        test_result_repo,
        sample_repo,
        parameter_repo,
        specification_repo,
        measurement_repo
    )
