from sqlalchemy.ext.asyncio.session import AsyncSession
from uuid import uuid4, UUID

from src.core.security.token import Token
from src.db.models import User
from src.core.config import settings
from src.db.unit_of_work import UnitOfWork
from src.db.repositories import AuthRepository
from src.core.security.utils import (
    decode_jwt,
    encode_jwt,
    verify_password,
    get_password_hash,
)
from .schemas import LoginSchema
from src.db.repositories import UserRepository
from datetime import datetime

from src.core.security.send_email import verify_verification_token
from src.core.exceptions.service.auth import (
    InvalidTokenError,
    TokenExpiredError,
    EmailNotExistsError,
    InvalidPasswordError,
)

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_FIELD = "access"
REFRESH_TOKEN_FIELD = "refresh"


class AuthService:
    def __init__(
        self,
        uow: UnitOfWork,
        user_repository: UserRepository,
        auth_repository: AuthRepository,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    def __create_token(
        self, payload: dict, token_type: str, expire_minutes: int
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(payload)
        return encode_jwt(jwt_payload, expire_minutes)

    def __create_refresh_token(self, email: str) -> str:
        payload = {
            "sub": email,
            "jti": str(uuid4()),
        }
        return self.__create_token(
            payload,
            REFRESH_TOKEN_FIELD,
            settings.auth_jwt.refresh_token_expire_days * 60 * 24,
        )

    def __create_access_token(self, user: User):
        payload = {
            "sub": user.email,
            "user_id": str(user.id),
        }
        return self.__create_token(
            payload, ACCESS_TOKEN_FIELD, settings.auth_jwt.access_token_expire_minutes
        )

    async def __create_tokens(
        self,
        session: AsyncSession,
        user_id: UUID,
        user: User | None = None,
    ):
        if not user:
            user = await self.user_repository.get_by_id(session, user_id)
        access_token = self.__create_access_token(user)
        refresh_token = self.__create_refresh_token(user.email)
        data = {}
        data.update(refresh_token=refresh_token, user_id=user_id)
        await self.auth_repository.create(session, data)
        await session.commit()
        return Token(
            access_token=access_token, refresh_token=refresh_token, type="Bearer"
        )

    async def create_token(self, user_id: UUID):
        async with self.uow as uow:
            return await self.__create_tokens(uow.session, user_id)

    async def logout(self, refresh_token: str):
        async with self.uow as uow:
            await self.auth_repository.delete_by_token(uow.session, refresh_token)
            await uow.session.commit()

    async def refresh_token(self, refresh_token: str):
        async with self.uow as uow:
            token = await self.auth_repository.get_by_filters(
                uow.session,
                {"refresh_token": refresh_token},
            )
            if token is None:
                raise InvalidTokenError
            payload = decode_jwt(token.refresh_token)
            if payload.get("type") != "refresh":
                raise InvalidTokenError
            email = payload["sub"]
            user = await self.user_repository.get_by_email(uow.session, email)
            expires_in = payload["exp"]
            if datetime.now().timestamp() >= expires_in:
                raise TokenExpiredError
            await uow.session.delete(token)
            await uow.commit()
            return await self.__create_tokens(uow.session, user.id, user)

    async def authenticate_user(self, data: LoginSchema):
        email = data.email
        password = data.password
        async with self.uow as uow:
            user = await self.user_repository.get_by_email(uow.session, email)
            if not user:
                raise EmailNotExistsError
            if not verify_password(password, user.password_hash):
                raise InvalidPasswordError
            return await self.__create_tokens(uow.session, user.id, user)

    async def abort_all_sessions(self, user_id):
        async with self.uow as uow:
            await self.auth_repository.delete_multi(
                session=uow.session, user_id=user_id
            )
            await uow.commit()

    async def change_password(self, email, old_password, new_password):
        async with self.uow as uow:
            user = await self.user_repository.get_by_email(uow.session, email)
            if verify_password(old_password, user.password_hash):
                user.password_hash = get_password_hash(new_password)
                await uow.commit()
            else:
                raise InvalidPasswordError

    async def verify_account(self, token: str):
        async with self.uow as uow:
            payload = verify_verification_token(token)
            if payload is None:
                raise InvalidTokenError

            email = payload["sub"]
            user = await self.user_repository.get_by_email(uow.session, email)
            if user is None:
                raise InvalidTokenError

            expires_in = payload["exp"]
            if datetime.now().timestamp() >= expires_in:
                raise TokenExpiredError

            user.is_verified = True
            await uow.commit()

    async def reset_password(self, token: str, new_password: str):
        """Сброс пароля по токену восстановления"""
        async with self.uow as uow:
            session = uow.session
            payload = verify_verification_token(token)
            if payload is None:
                raise InvalidTokenError

            email = payload["sub"]
            user = await self.user_repository.get_by_email(session, email)
            if user is None:
                raise InvalidTokenError

            expires_in = payload["exp"]
            if datetime.now().timestamp() >= expires_in:
                raise TokenExpiredError

            user.password_hash = get_password_hash(new_password)
            # Завершаем все активные сессии пользователя для безопасности
            await self.auth_repository.delete_multi(session=session, user_id=user.id)
            await uow.commit()
