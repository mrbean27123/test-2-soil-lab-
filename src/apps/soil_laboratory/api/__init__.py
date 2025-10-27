from fastapi import APIRouter

from apps.soil_laboratory.api.material_sources import router as material_sources_router
from apps.soil_laboratory.api.material_types import router as material_types_router
from apps.soil_laboratory.api.materials import router as materials_router
from apps.soil_laboratory.api.parameters import router as parameters_router
from apps.soil_laboratory.api.samples import router as samples_router
from apps.soil_laboratory.api.test_results import router as tests_router


router = APIRouter(prefix="/v1")

router.include_router(material_sources_router)
router.include_router(material_types_router)
router.include_router(materials_router)
router.include_router(parameters_router)
router.include_router(samples_router)
router.include_router(tests_router)
