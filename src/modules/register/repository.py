from core.abstract.repository import AbstractRepository
from core.abstract.sqla_repo import SQLAlchemyRepository

from modules.user.models import User
from modules.profile.models import Profile # noqa


# Я импортирую модель Profile во избежание ошибки SQLAlchemy, которая
# гласит о том, что маппер не может найти такую таблицу

class RegisterRepository(SQLAlchemyRepository):
    model = User

    async def add_one(self, data: dict):
        return await super().add_one(data)

    async def find_all(self, filter_by: dict):
        return await super().find_all(filter_by)
