from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.classes import Annotations, Base
from .role import Role


class User(Base):
    __tablename__ = 'user'

    id: Mapped[Annotations.primary_id]
    role: Mapped[Role] = mapped_column(default=Role.USER)

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    is_activated: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[Annotations.created_at]
    updated_at: Mapped[Annotations.updated_at]

    # profile = relationship("Profile", uselist=False)
