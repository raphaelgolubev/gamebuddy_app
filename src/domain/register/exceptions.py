from fastapi import status
from fastapi.responses import JSONResponse

from core.utils.logging.logger import AppLogger


logger = AppLogger(__name__)


class UserAlreadyExistsError(Exception): 
    pass


async def user_already_exists(request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={
            "code": 1001,
            "detail": "Пользователь с таким адресом электронной почты уже существует"
        }
    )
