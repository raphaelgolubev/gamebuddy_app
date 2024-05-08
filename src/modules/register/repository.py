from core.abstract.repository import AbastractRepository
from core.abstract.sqla_repo import SQLAlchemyRepository

from modules.user.models import User


class RegisterRepository(SQLAlchemyRepository):
    model = User


class RegisterService:
    def __init__(self, register_repo: AbastractRepository):
        self.register_repo: AbastractRepository = register_repo()
