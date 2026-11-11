
"""Mock token authentication (no real login, no passwords)."""

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.errors import ApiError

USERS = {
    "user-a-token": {"id": "user-a", "name": "User A", "role": "user"},
    "user-b-token": {"id": "user-b", "name": "User B", "role": "user"},
    "admin-token": {"id": "admin", "name": "Administrator", "role": "admin"},
}

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)
) -> dict:
    """Dependency: returns the user for the Bearer token or raises 401."""

    if credentials is None:
        raise ApiError(
            401,
            "UNAUTHORIZED",
            "Authorization header is missing or invalid. Use: Bearer <token>."
        )

    token = credentials.credentials
    user = USERS.get(token)

    if user is None:
        raise ApiError(
            401,
            "UNAUTHORIZED",
            "The token is invalid."
        )

    return user
