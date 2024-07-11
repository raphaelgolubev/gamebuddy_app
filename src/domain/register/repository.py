from core.database.sqla_repo import SQLAlchemyRepository

from entities.models.user import User
# from modules.profile.models import Profile # noqa


# Я импортирую модель Profile во избежание ошибки SQLAlchemy, которая
# гласит о том, что маппер не может найти такую таблицу

class RegisterRepository(SQLAlchemyRepository):
    model = User
