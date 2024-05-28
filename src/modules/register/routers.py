from fastapi import APIRouter

from .schemas import RegisterIn, RegisterOut

from core.dependencies import get_register_service


router = APIRouter(prefix="/register", tags=["Регистрация"])

# Список ошибок
# 1000 - регистрация
# 1001 - пользователь с таким email уже существует
# 1002 - пользователь не найден
# 1003 - код неверный
# 1004 - время действия кода истекло


# TODO: добавить обработку ошибок, покрыть тестами
@router.post("/create", summary="Создает нового пользователя в базе данных")
async def create_user(user: RegisterIn) -> RegisterOut:
    """
    Метод принимает запрос в формате JSON:
    - **email**: электронная почта пользователя
    - **password**: пароль пользователя
    Возвращает:
    - идентификатор пользователя в базе данных

    Метод может вернуть следующие ошибки:
    - **1001**: пользователь с таким email уже существует
    """
    service = get_register_service()
    created = await service.create_user(user.model_dump())

    return created


@router.post("/verify", summary="Обновляет статус пользователя")
async def verify_user():
    """
    Метод принимает запрос в формате JSON:
    - **email**: электронная почта пользователя
    - **code**: код подтверждения пользователя, высланный на почту

    Метод может вернуть следующие ошибки:
    - **1002**: пользователь не найден
    - **1003**: код неверный

    """
    pass


@router.post("/send-code", summary="Отправляет код подтверждения на почту")
async def send_code():
    """
    Метод принимает запрос в формате JSON:
    """
    pass
