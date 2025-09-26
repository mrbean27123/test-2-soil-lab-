from fastapi import APIRouter

from apps.soil_laboratory.api.samples import router as samples_router
from apps.soil_laboratory.api.tests import router as tests_router


router = APIRouter(prefix="/v1")

router.include_router(samples_router)
router.include_router(tests_router)
