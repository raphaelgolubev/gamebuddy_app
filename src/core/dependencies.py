from modules.user.models import User

from modules.register.repository import RegisterRepository
from modules.register.service import RegisterService

from core.application import GameBuddyApp


def get_gamebuddy_app() -> GameBuddyApp:
    return GameBuddyApp()


def get_register_service():
    repo = RegisterRepository(model=User)
    return RegisterService(repo)
