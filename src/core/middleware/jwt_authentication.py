from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.security.interfaces import JWTManagerInterface


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, jwt_manager: JWTManagerInterface):
        super().__init__(app)
        self.jwt_manager = jwt_manager
        self.exclude_paths = ["/auth", "/health", "/docs", "/openapi.json"]

    @staticmethod
    def _extract_endpoint_path(full_path: str) -> str:
        parts = full_path.split("/", 3)

        if len(parts) >= 3 and parts[1] == "api" and parts[2].startswith("v"):
            return "/" + (parts[3] if len(parts) > 3 else "")

        return full_path

    async def dispatch(self, request: Request, call_next):
        original_path = request.url.path
        endpoint_path = self._extract_endpoint_path(original_path)

        # Skip authentication for excluded paths
        if any(endpoint_path.startswith(excluded) for excluded in self.exclude_paths):
            return await call_next(request)

        # Get authorization header
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header is missing"}
            )

        scheme, _, token = authorization_header.partition(" ")

        if scheme != "Bearer" or not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid Authorization header format. Expected 'Bearer <token>'"}
            )

        # Decode and validate JWT token
        payload = self.jwt_manager.decode_access_token(token)

        # Extract user data from JWT payload
        user_data = {
            "user_id": payload.get("sub"),
            "email": payload.get("email")
        }
        print(user_data)

        # Add user data to request state
        request.state.user_id = payload.get("sub")
        request.state.user_email = payload.get("email")

        # Continue to the next middleware or endpoint
        return await call_next(request)
