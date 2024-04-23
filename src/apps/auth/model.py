from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, Annotations


class Role(Enum):
    GUEST = 'GUEST'
    USER = 'USER'
    MODERATOR = 'MODERATOR'
    ADMIN = 'ADMIN'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[Annotations.primary_id]
    role: Mapped[Role] = mapped_column(default=Role.USER)
    created_at: Mapped[Annotations.created_at]
    updated_at: Mapped[Annotations.updated_at]
