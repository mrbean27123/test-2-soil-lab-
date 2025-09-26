from pydantic import BaseModel

from apps.identity.schemas.auth.jwt import (  # noqa: F401
    LoginRequest,
    LogoutRequest,
    TokenPairResponse,
    TokenRefreshRequest,
    TokenRefreshResponse
)
from apps.identity.schemas.auth.user_data import UserData  # noqa: F401
from apps.identity.schemas.permission import (  # noqa: F401
    PermissionCreate,
    PermissionDetailResponse,
    PermissionListItemResponse,
    PermissionListResponse,
    PermissionLookupResponse,
    PermissionShortResponse,
    PermissionUpdate
)
from apps.identity.schemas.role import (  # noqa: F401
    RoleCreate,
    RoleDetailResponse,
    RoleListItemResponse,
    RoleListResponse,
    RoleLookupResponse,
    RoleShortResponse,
    RoleUpdate
)
from apps.identity.schemas.user import (  # noqa: F401
    UserCreate,
    UserDetailResponse,
    UserListItemResponse,
    UserListResponse,
    UserLookupResponse,
    UserShortResponse,
    UserUpdate
)
from apps.soil_laboratory.schemas.sample import (  # noqa: F401
    SampleCreate,
    SampleDetailResponse,
    SampleListItemResponse,
    SampleListResponse,
    SampleLookupResponse,
    SampleShortResponse,
    SampleUpdate
)
from apps.soil_laboratory.schemas.test import (  # noqa: F401
    TestCreate,
    TestDetailResponse,
    TestListItemResponse,
    TestListResponse,
    TestLookupResponse,
    TestShortResponse,
    TestUpdate
)


# Rebuild Pydantic models to resolve forward references (string annotations)
# This is required for schemas that use string type hints to avoid circular imports and ensure
# proper OpenAPI schema generation
schemas_to_rebuild: list[type[BaseModel]] = [
    SampleDetailResponse,
    TestDetailResponse,
    SampleListItemResponse,

    RoleDetailResponse,
    RoleListItemResponse,

    UserDetailResponse,
    UserListItemResponse
]

for schema in schemas_to_rebuild:
    try:
        schema.model_rebuild()
    except Exception as e:
        print(f"Failed to rebuild {schema.__name__}: {e}")
