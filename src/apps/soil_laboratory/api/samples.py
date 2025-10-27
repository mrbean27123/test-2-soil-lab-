from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from starlette.responses import StreamingResponse

from apps.identity.dependencies.auth import require_permission
from apps.identity.schemas import UserData
from apps.soil_laboratory.dependencies.services import get_sample_report_service, get_sample_service
from apps.soil_laboratory.schemas.sample import (
    SampleCreate,
    SampleDetailResponse,
    SamplePaginatedListResponse,
    SamplesReportGenerationRequest
)
from apps.soil_laboratory.services.reports.sample_report import SampleReportService
from apps.soil_laboratory.services.sample import SampleService


router = APIRouter(prefix="/samples", tags=["samples"])


@router.get("/", response_model=SamplePaginatedListResponse)
async def get_samples_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    sample_service: SampleService = Depends(get_sample_service),
    current_user: UserData = Depends(require_permission("samples.read"))
) -> SamplePaginatedListResponse:
    return await sample_service.get_samples_paginated(page, per_page)


@router.post("/", response_model=SampleDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_sample(
    sample_data: SampleCreate,
    sample_service: SampleService = Depends(get_sample_service),
    current_user: UserData = Depends(require_permission("samples.create"))
) -> SampleDetailResponse:
    return await sample_service.create_sample(sample_data)


@router.get("/{sample_id:uuid}", response_model=SampleDetailResponse)
async def get_sample(
    sample_id: UUID,
    sample_service: SampleService = Depends(get_sample_service),
    current_user: UserData = Depends(require_permission("samples.read"))
) -> SampleDetailResponse:
    return await sample_service.get_sample_by_id(sample_id)


@router.delete("/{sample_id}", response_model=SampleDetailResponse)
async def delete_sample(
    sample_id: UUID,
    sample_service: SampleService = Depends(get_sample_service),
    current_user: UserData = Depends(require_permission("samples.delete"))
) -> SampleDetailResponse:
    return await sample_service.delete_sample(sample_id)


@router.post("/{sample_id}/restore", response_model=SampleDetailResponse)
async def restore_sample(
    sample_id: UUID,
    sample_service: SampleService = Depends(get_sample_service),
    current_user: UserData = Depends(require_permission("samples.restore"))
) -> SampleDetailResponse:
    return await sample_service.restore_sample(sample_id)


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
async def get_samples_report(
    report_generation_request: SamplesReportGenerationRequest,
    sample_report_service: SampleReportService = (
        Depends(get_sample_report_service)
    ),
    current_user: UserData = Depends(require_permission("samples.read"))
):
    response_data, file_buffer = await sample_report_service.generate_samples_report(
        report_generation_request
    )

    return StreamingResponse(
        file_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename={response_data.file_name}",
            "X-Report-Metadata": response_data.model_dump_json()
        }
    )
