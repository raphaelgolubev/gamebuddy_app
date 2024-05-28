from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import ForeignKey

from src.core.database import Annotations, Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user.models import User


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[Annotations.primary_id]
    user: Mapped["User"] = relationship(back_populates="profile", uselist=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
