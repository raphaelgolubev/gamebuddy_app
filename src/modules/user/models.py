from enum import Enum
from tokenize import String
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import ForeignKey

from core.database import Annotations, Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from profile.models import Profile


class Role(Enum):
    GUEST = "GUEST"
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "user"

    id: Mapped[Annotations.primary_id]
    role: Mapped[Role] = mapped_column(default=Role.USER)

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    is_activated: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False) 

    created_at: Mapped[Annotations.created_at]
    updated_at: Mapped[Annotations.updated_at]
