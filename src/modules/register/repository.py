from core.abstract.repository import AbstractRepository
from core.abstract.sqla_repo import SQLAlchemyRepository

from modules.user.models import User


class RegisterRepository(SQLAlchemyRepository):
    model = User


class RegisterService:
    def __init__(self, register_repo: AbstractRepository):
        self.register_repo: AbstractRepository = register_repo
