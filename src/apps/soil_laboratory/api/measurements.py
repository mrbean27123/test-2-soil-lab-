from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from starlette.responses import StreamingResponse

from apps.identity.dependencies.auth import require_login, require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies import (
    get_measurement_service,
    get_measurements_report_service
)
from apps.soil_laboratory.schemas.measurement import (
    MeasurementCreate,
    MeasurementDetailResponse,
    MeasurementListResponse,
    MeasurementLookupResponse,
    MeasurementUpdate, MeasurementsReportGenerationRequest,
)
from apps.soil_laboratory.services.measurement import MeasurementService
from apps.soil_laboratory.services.reports.measurement_reports import MeasurementsReportService


router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.get("/lookups", response_model=list[MeasurementLookupResponse])
async def get_permission_lookups_list(
    limit: int | None = Query(75, ge=1, le=500),
    search: str | None = Query(None, min_length=2, max_length=50),
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_login())
) -> list[MeasurementLookupResponse]:
    return await measurement_service.get_measurement_lookup_options(limit=limit, search=search)


@router.get("/", response_model=MeasurementListResponse)
async def get_measurements_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_permission("measurements.read"))
) -> MeasurementListResponse:
    return await measurement_service.get_measurements_paginated(page=page, per_page=per_page)


@router.post("/", response_model=MeasurementDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_measurement(
    measurement_data: MeasurementCreate,
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_permission("measurements.create"))
) -> MeasurementDetailResponse:
    return await measurement_service.create_measurement(measurement_data)


@router.get("/{measurement_id:uuid}", response_model=MeasurementDetailResponse)
async def get_measurement(
    measurement_id: UUID,
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_permission("measurements.read"))
) -> MeasurementDetailResponse:
    return await measurement_service.get_measurement_by_id(measurement_id)


@router.put("/{measurement_id}", response_model=MeasurementDetailResponse)
async def update_measurement(
    measurement_id: UUID,
    measurement_data: MeasurementUpdate,
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_permission("measurements.update"))
) -> MeasurementDetailResponse:
    return await measurement_service.update_measurement(measurement_id, measurement_data)


@router.delete("/{measurement_id}", response_model=MeasurementDetailResponse)
async def delete_measurement(
    measurement_id: UUID,
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_permission("measurements.delete"))
) -> MeasurementDetailResponse:
    return await measurement_service.delete_measurement(measurement_id)


@router.post("/{measurement_id}/restore", response_model=MeasurementDetailResponse)
async def restore_measurement(
    measurement_id: UUID,
    measurement_service: MeasurementService = Depends(get_measurement_service),
    current_user: UserData = Depends(require_permission("measurements.restore"))
) -> MeasurementDetailResponse:
    return await measurement_service.restore_measurement(measurement_id)


@router.post(
    "/generate-report",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
            "description": "DOCX report file",
        }
    },
)
async def get_measurements_report(
    report_generation_request: MeasurementsReportGenerationRequest,
    measurement_report_service: MeasurementsReportService = (
        Depends(get_measurements_report_service)
    ),
    current_user: UserData = Depends(require_permission("measurements.read"))
):
    response_data, file_buffer = await measurement_report_service.generate_measurements_report(
        report_generation_request
    )

    # Возвращаем файл как потоковый ответ
    return StreamingResponse(
        file_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename={response_data.file_name}",
            "X-Report-Metadata": response_data.model_dump_json()
        }
    )
