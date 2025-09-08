from fastapi import APIRouter

from apps.soil_laboratory.api.measurements import router as measurements_router


router = APIRouter(prefix="/v1")

router.include_router(measurements_router)
