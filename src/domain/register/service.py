from core.abc.repository import AbstractRepository
from .schemas import RegisterOut


class RegisterService:
    def __init__(self, register_repo: AbstractRepository):
        self.register_repo: AbstractRepository = register_repo

    async def create_user(self, data: dict) -> RegisterOut:
        db_res = await self.register_repo.add_one(data)
        return RegisterOut(**db_res)
