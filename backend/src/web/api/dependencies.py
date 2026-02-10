from datetime import datetime, UTC
from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.exceptions.service.auth import TokenExpiredError, InvalidTokenError
from src.core.exceptions.service.base import ForbiddenError, NoAccessError
from src.core.security.utils import decode_jwt
from src.db.models.mixins import Role
from src.services.auth.service import AuthService, TOKEN_TYPE_FIELD, ACCESS_TOKEN_FIELD
from src.services.dependencies import get_auth_service, get_user_service
from src.services.user.schemas import UserDTO
from src.services.user.service import UserService

# Service dependencies


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

# Auth Dependencies

http_bearer = HTTPBearer()



def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    payload = decode_jwt(token)
    exp = payload["exp"]
    if exp < datetime.now(UTC).timestamp():
        raise TokenExpiredError()
    return payload


async def get_token_for_refresh(
    request: Request,
) -> str:
    token = request.cookies.get("refresh_token")
    if token:
        return token
    raise InvalidTokenError("No token")


async def get_current_user(
    service: UserServiceDep,
    payload: dict = Depends(get_current_token_payload),
) -> UserDTO:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_FIELD:
        raise InvalidTokenError("Invalid token type")
    email = payload.get("sub")
    if not email:
        raise InvalidTokenError()
    user = await service.get_by_email(email)
    return user


async def get_current_active_user(
    user: UserDTO = Depends(get_current_user),
) -> UserDTO:
    if not user.is_active:
        raise ForbiddenError(
            detail="User inactive",
        )
    return user


async def get_current_verified_user(
    user: UserDTO = Depends(get_current_active_user),
) -> UserDTO:
    """Проверяет что пользователь верифицировал email"""
    if not user.is_verified:
        raise ForbiddenError(
            "Email not verified. Please verify your email address.",
        )
    return user


async def get_current_superuser(
    user: UserDTO = Depends(get_current_active_user),
) -> UserDTO:
    if not (user.role == Role.ADMIN):
        raise NoAccessError()
    return user

CurrentUserDep = Annotated[UserDTO, Depends(get_current_active_user)]
CurrentVerifiedUserDep = Annotated[UserDTO, Depends(get_current_verified_user)]
