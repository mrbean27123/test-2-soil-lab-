from fastapi import APIRouter

from apps.identity.api.auth import router as auth_router
from apps.identity.api.permissions import router as permissions_router
from apps.identity.api.roles import router as roles_router
from apps.identity.api.users import router as users_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(permissions_router)
router.include_router(roles_router)
router.include_router(users_router)
