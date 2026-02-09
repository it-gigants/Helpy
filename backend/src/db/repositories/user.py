from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQlAlchemyRepository
from src.db.models import User


class UserRepository(SQlAlchemyRepository):
    model = User

    async def get_by_email(self, session: AsyncSession, email: str):
        return await self.get_by_filters(session, {"email": email})
