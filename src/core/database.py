from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from core.config import settings


class Base(DeclarativeBase):
    pass


class Annotations:
    """Класс с аннотациями для переиспользуемости кода в объявлении таблиц"""

    primary_id = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
    created_at = Annotated[
        datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
    ]
    updated_at = Annotated[
        datetime,
        mapped_column(
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=text("TIMEZONE('utc', now())"),
        ),
    ]


async_engine = create_async_engine(
    settings.database.asyncpg_url,
    echo=True,
    pool_size=10,
    max_overflow=10,
)
async_session_factory = async_sessionmaker(async_engine)


# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
