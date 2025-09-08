from fastapi import FastAPI

from apps.identity.api import router as identity_app_router
from apps.soil_laboratory.api import router as soil_laboratory_app_router
from core.config import settings
from core.logging_config import logger
from core.middleware import (
    ErrorHandlingMiddleware,
    JWTAuthenticationMiddleware,
    RequestLoggingMiddleware
)
from core.security.dependencies import get_jwt_manager

# Rebuild Schemas
import schemas.to_rebuild  # noqa: F401

# Register ORM Models
import database.models.all_models  # noqa: F401


app = FastAPI(title=settings.APP_NAME)

# NOTE: Middlewares are applied in **reverse order** (last added == outermost).
# The first middleware added becomes the **innermost** in the actual execution chain.
# So logging should go around error handling to ensure request is properly logged.

app.add_middleware(JWTAuthenticationMiddleware, jwt_manager=get_jwt_manager())  # Innermost middleware
app.add_middleware(ErrorHandlingMiddleware, logger=logger)
app.add_middleware(RequestLoggingMiddleware, logger=logger)  # Outermost middleware

app.include_router(identity_app_router, prefix="/api")
app.include_router(soil_laboratory_app_router, prefix="/api")
