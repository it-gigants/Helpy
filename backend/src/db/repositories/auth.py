from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from src.db.models import RefreshSession
from src.db.repositories.base import SQlAlchemyRepository


class AuthRepository(SQlAlchemyRepository):
    model = RefreshSession

    async def delete_multi(self, session: AsyncSession, **filters):
        stmt = delete(RefreshSession).filter_by(**filters)
        await session.execute(stmt)
        await session.flush()

    async def delete_by_token(self, session: AsyncSession, token: str):
        stmt = delete(RefreshSession).filter_by(refresh_token=token)
        await session.execute(stmt)
        await session.flush()
