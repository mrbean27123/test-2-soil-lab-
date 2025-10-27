from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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
from schemas.utils import resolve_schemas_forward_refs

# Register ORM Models
import database.models.all_models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup and shutdown events."""
    # Startup
    # logger.info("Application startup: initializing resources...")

    # Rebuild Schemas
    resolve_schemas_forward_refs("src/apps")

    yield

    # Shutdown
    # logger.info("Application shutdown: cleaning up resources...")
    # ...
    # logger.info("Application shutdown complete")


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# NOTE: Middlewares are applied in **reverse order** (last added == outermost).
# The first middleware added becomes the **innermost** in the actual execution chain.
# So logging should go around error handling to ensure request is properly logged.

app.add_middleware(JWTAuthenticationMiddleware, jwt_manager=get_jwt_manager())
app.add_middleware(ErrorHandlingMiddleware, logger=logger)
app.add_middleware(RequestLoggingMiddleware, logger=logger)  # Outermost middleware

# TODO: Remove this:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(identity_app_router, prefix="/api")
app.include_router(soil_laboratory_app_router, prefix="/api")
