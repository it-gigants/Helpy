from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import insert, select, delete, inspect, update
from sqlalchemy.sql.elements import ColumnElement

class SQlAlchemyRepository:
    model = None

    async def create(self, session: AsyncSession, data: dict):
        mapper = inspect(self.model)
        data_to_create = {}
        for key, value in data.items():
            if key in mapper.columns:
                data_to_create[key] = value
        stmt = insert(self.model).values(**data_to_create).returning(self.model)
        result = await session.execute(stmt)
        return result.scalar()

    async def get_all(self, session: AsyncSession):
        res = await session.scalars(select(self.model))
        return [user for user in res]

    async def get_by_filters(
            self, session: AsyncSession, filters: dict, one: bool = True
    ):
        stmt = select(self.model).filter_by(**filters)
        res = await session.execute(stmt)
        if one:
            return res.scalar_one_or_none()
        return res.scalars().all()

    async def delete_by_id(
            self, session: AsyncSession, entity_id: Any | ColumnElement[Any]
    ):
        await session.execute(delete(self.model).where(self.model.id == str(entity_id)))

    async def get_by_id(self, session: AsyncSession, id: Any | ColumnElement[Any]):
        return await session.get(self.model, id)

    async def update(self, session: AsyncSession, entity_id: UUID, data: dict):
        mapper = inspect(self.model)
        data_to_update = {}
        for key, value in data.items():
            if key in mapper.columns:
                data_to_update[key] = value

        if not data_to_update:
            return

        stmt = (
            update(self.model).where(self.model.id == entity_id).values(**data_to_update)
        )
        await session.execute(stmt)
