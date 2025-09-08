from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.identity.dependencies.repositories import (
    get_permission_repository,
    get_role_repository,
    get_token_repository,
    get_user_repository
)
from apps.identity.repositories import (
    PermissionRepository,
    RoleRepository,
    TokenRepository,
    UserRepository
)
from apps.identity.services import AuthService, PermissionService, RoleService, UserService
from core.security.dependencies import get_jwt_manager
from core.security.interfaces import JWTManagerInterface
from database.dependencies import get_postgresql_db_session as get_db_session


def get_auth_service(
    db: AsyncSession = Depends(get_db_session),
    jwt_manager: JWTManagerInterface = Depends(get_jwt_manager),
    user_repo: UserRepository = Depends(get_user_repository),
    token_repo: TokenRepository = Depends(get_token_repository),
) -> AuthService:
    return AuthService(db, jwt_manager, user_repo, token_repo)


def get_permission_service(
    db: AsyncSession = Depends(get_db_session),
    permission_repo: PermissionRepository = Depends(get_permission_repository)
) -> PermissionService:
    return PermissionService(db, permission_repo)


def get_role_service(
    db: AsyncSession = Depends(get_db_session),
    role_repo: RoleRepository = Depends(get_role_repository),
    permission_repo: PermissionRepository = Depends(get_permission_repository)
) -> RoleService:
    return RoleService(db, role_repo, permission_repo)


def get_user_service(
    db: AsyncSession = Depends(get_db_session),
    user_repo: UserRepository = Depends(get_user_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    permission_repo: PermissionRepository = Depends(get_permission_repository)
) -> UserService:
    return UserService(db, user_repo, role_repo, permission_repo)
