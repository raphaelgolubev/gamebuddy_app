from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.classes import Base, Annotations


class Profile(Base):
    __tablename__ = 'profile'

    id: Mapped[Annotations.primary_id]

    created_at: Mapped[Annotations.created_at]
    updated_at: Mapped[Annotations.updated_at]

    user = relationship("User", back_populates="profile")
