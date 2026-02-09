from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security.utils import get_password_hash
from src.core.exceptions.service.base import (
    NotFoundError,
    AlreadyExistsError,
)
from src.db.models import User
from src.db.repositories import UserRepository
from .schemas import (
    UserDTO,
    SUserCreate,
)


class UserService:
    def __init__(self, unit_of_work, user_repository: UserRepository):
        self.uow = unit_of_work
        self.repository = user_repository

    async def _get_user_by_id(self, session: AsyncSession, id: str):
        u = await session.get(User, id)
        if not u:
            raise NotFoundError("User not found")
        return u

    async def get_by_email(self, email: EmailStr) -> UserDTO:
        async with self.uow as uow:
            session = uow.session
            res = await self.repository.get_by_email(session, str(email))
            return UserDTO.model_validate(res)

    async def _validate_email(self, email: EmailStr, session: AsyncSession):
        u = await self.repository.get_by_email(session, str(email))
        if u:
            raise AlreadyExistsError(f"Email {email} already exists")

    async def create(self, data: SUserCreate) -> UserDTO:
        async with self.uow as uow:
            session = uow.session
            await self._validate_email(data.email, session)
            data_to_create = data.model_dump()
            pwd_hash = get_password_hash(data_to_create.pop("password"))
            data_to_create.update(password_hash=pwd_hash)
            res = await self.repository.create(session, data_to_create)
            await session.commit()
            return UserDTO.model_validate(res)

    async def mark_user_inactive(self, id: str) -> None:
        async with self.uow as uow:
            session = uow.session
            user = await self._get_user_by_id(session, id)
            user.is_active = False
            await session.commit()

    async def mark_user_active(self, id: str) -> None:
        async with self.uow as uow:
            session = uow.session
            user = await self._get_user_by_id(session, id)
            user.is_active = True
            await session.commit()

    async def get_all(self):
        async with self.uow as uow:
            session = uow.session
            res = await self.repository.get_by_filters(
                session, {"is_active": True}, one=False
            )
            return [UserDTO.model_validate(res) for res in res]


