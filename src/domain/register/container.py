from entities.models.user import User

from domain.register.repository import RegisterRepository
from domain.register.service import RegisterService


def get_register_service():
    repo = RegisterRepository(model=User)
    return RegisterService(repo)
