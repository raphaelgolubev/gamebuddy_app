from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column


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