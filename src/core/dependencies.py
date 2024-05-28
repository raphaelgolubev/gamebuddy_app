from modules.user.models import User

from modules.register.repository import RegisterRepository
from modules.register.service import RegisterService


def get_register_service():
    repo = RegisterRepository(model=User)
    return RegisterService(repo)
