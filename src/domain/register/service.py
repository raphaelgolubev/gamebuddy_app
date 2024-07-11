import uuid

from core.abc.repository import AbstractRepository
from core.security.hasher import Hasher

from .exceptions import UserAlreadyExistsError
from .schemas import RegisterOut

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


class RegisterService:
    def __init__(self, register_repo: AbstractRepository):
        self.register_repo: AbstractRepository = register_repo

    def _hash_password(self, password: str) -> str:
        return Hasher.get_password_hash(password)

    async def create_user(self, data: dict) -> RegisterOut:
        id = uuid.uuid4()

        data.update(
            {
                "password": self._hash_password(data["password"])
            }
        )

        try:
            db_res = self.register_repo.create(data=data)
            id = db_res.inserted_primary_key[0]
            return RegisterOut(id=id)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise UserAlreadyExistsError()

        return RegisterOut(id=id)
