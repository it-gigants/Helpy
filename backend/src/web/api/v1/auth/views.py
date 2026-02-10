from fastapi import APIRouter, Depends, Response, BackgroundTasks
from pydantic import BaseModel, EmailStr
from fastapi.responses import HTMLResponse

from src.web.api.dependencies import (
    AuthServiceDep,
    UserServiceDep,
    CurrentUserDep,
    get_token_for_refresh,
    get_current_verified_user,
    get_current_active_user,
)
from src.core.exceptions.service.base import BadRequestError
from loguru import logger
from src.core.security.send_email import (
    send_verification_email,
    send_password_reset_email,
)
from src.core.security.token import Token
from src.core.config import settings
from src.core.exceptions.service.auth import TokenExpiredError, InvalidTokenError
from src.services.auth.schemas import LoginSchema, RegisterSchema
from src.services.user.schemas import UserDTO, SUserCreate

router = APIRouter()

@router.get("/me")
async def get_user(
    user: UserDTO = Depends(get_current_verified_user),
) -> UserDTO:
    return user


@router.post("/login")
async def login(
    data: LoginSchema,
    service: AuthServiceDep,
    response: Response,
) -> Token:
    tokens = await service.authenticate_user(data)
    response.set_cookie(
        "refresh_token",
        tokens.refresh_token,
        max_age=settings.auth_jwt.refresh_token_expire_days * 60 * 24 * 60,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return tokens


@router.post("/register")
async def register(
    data: RegisterSchema,
    user_service: UserServiceDep,
    service: AuthServiceDep,
    background_tasks: BackgroundTasks,
    response: Response,
):
    await user_service.create(SUserCreate(**data.model_dump()))
    background_tasks.add_task(send_verification_email, str(data.email))
    tokens = await service.authenticate_user(
        LoginSchema(
            email=data.email,
            password=data.password,
        )
    )
    response.set_cookie(
        "refresh_token",
        tokens.refresh_token,
        max_age=settings.auth_jwt.refresh_token_expire_days * 60 * 24 * 60,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return tokens


@router.post("/refresh")
async def refresh_jwt(
    response: Response,
    service: AuthServiceDep,
    token=Depends(get_token_for_refresh),
) -> Token:
    tokens = await service.refresh_token(token)
    response.set_cookie(
        "refresh_token",
        tokens.refresh_token,
        max_age=settings.auth_jwt.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return tokens


@router.post("/logout")
async def logout(
    service: AuthServiceDep,
    response: Response,
    token=Depends(get_token_for_refresh),
) -> None:
    await service.logout(token)
    response.delete_cookie("refresh_token")


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str


@router.post("/change_password")
async def change_password(
    service: AuthServiceDep,
    data: ChangePasswordSchema,
    user: CurrentUserDep,
):
    await service.change_password(user.email, data.old_password, data.new_password)
    return {"message": "ok"}


@router.post("/quit_all")
async def quit_all(
    service: AuthServiceDep,
    response: Response,
    user: CurrentUserDep,
):
    await service.abort_all_sessions(user.id)
    response.delete_cookie("refresh_token")
    return {"message": "ok"}


@router.get("/verify", response_class=HTMLResponse)
async def verify_account(
    token: str,
    service: AuthServiceDep,
):
    try:
        await service.verify_account(token)
        return "<h3>Ваш аккаунт успешно подтверждён ✅</h3>"
    except (InvalidTokenError, TokenExpiredError):
        return "<h3>Неверная или просроченная ссылка</h3>"


@router.post("/resend_verification")
async def resend_verification(
    background_tasks: BackgroundTasks,
    user: UserDTO = Depends(get_current_active_user),
):
    if user.is_verified:
        raise BadRequestError(detail="Email уже подтвержден")

    background_tasks.add_task(send_verification_email, str(user.email))
    return {"message": "Письмо с верификацией отправлено"}


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


@router.post("/forgot_password")
async def forgot_password(
    data: ForgotPasswordSchema,
    background_tasks: BackgroundTasks,
    user_service: UserServiceDep,
):
    """
    Запрос на восстановление пароля.
    Отправляет письмо с токеном для сброса пароля.
    Всегда возвращает успех, чтобы не раскрывать существование email в системе.
    """
    # Проверяем существование пользователя
    try:
        user = await user_service.get_by_email(data.email)
        if user:
            background_tasks.add_task(send_password_reset_email, str(data.email))
    except Exception as e:
        # Игнорируем любые ошибки, чтобы не раскрывать информацию о существовании email
        logger.warning(
            f"Ошибка при запросе восстановления пароля для {data.email}: {e}"
        )
    return {
        "message": "Если указанный email зарегистрирован, на него будет отправлено письмо с инструкцией по восстановлению пароля"
    }


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str


@router.post("/reset_password")
async def reset_password(
    data: ResetPasswordSchema,
    service: AuthServiceDep,
):
    """
    Сброс пароля по токену из письма.
    """
    try:
        await service.reset_password(data.token, data.new_password)
        return {"message": "Пароль успешно изменен"}
    except (InvalidTokenError, TokenExpiredError):
        raise BadRequestError(detail="Неверный или просроченный токен")
