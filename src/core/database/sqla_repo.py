from typing import Type

from sqlalchemy import insert, select, Connection
from core.abc.repository import AbstractRepository

from core.database.classes import Base
from core.database.connection import engine

from functools import wraps


def with_session_factory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with engine.connect() as conn:
            return func(conn, *args, **kwargs)

    return wrapper


class AsyncSQLAlchemyRepository(AbstractRepository):
    def __init__(self, model: Type[Base]) -> None:
        self.model = model

    @with_session_factory
    async def get(self, session, filter_by):
        return await super().get(filter_by)

    @with_session_factory
    async def create(self, session, data):
        return await super().create(data)

    @with_session_factory
    async def update(self, session, data):
        return await super().update(data)

    @with_session_factory
    async def delete(self, session, data):
        return await super().delete(data)

    @with_session_factory
    async def add_one(self, session, data: dict):
        stmt = insert(self.model).values(**data).returning(*self.model.__table__.columns)
        result = await session.execute(stmt)
        await session.commit()
        row = result.fetchone()
        return dict(row._mapping) if row is not None else None

    @with_session_factory
    async def find_all(self, session, filter_by: dict):
        stmt = select(self.model)
        result = await session.execute(stmt)

        return result


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, model: Type[Base]) -> None:
        self.model = model

    @with_session_factory
    def create(self, conn: Connection, data):
        stmt = (
            insert(self.model).
            values(**data)
        )
        result = conn.execute(stmt)
        conn.commit()

        return result

    def get(self, conn: Connection, filter_by):
        ...

    def update(self, conn: Connection, data):
        ...

    def delete(self, conn: Connection, data):
        ...
