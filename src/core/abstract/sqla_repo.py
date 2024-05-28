from typing import Type

from sqlalchemy import insert, select
from .repository import AbstractRepository

from core.database import Base, async_session_factory


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, model: Type[Base]) -> None:
        self.model = model

    async def add_one(self, data: dict):
        async with async_session_factory() as session:
            stmt = insert(self.model).values(**data).returning(*self.model.__table__.columns)
            result = await session.execute(stmt)
            await session.commit()
            row = result.fetchone()
            return dict(row._mapping) if row is not None else None

    async def find_all(self, filter_by: dict):
        async with async_session_factory() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)

            return result
