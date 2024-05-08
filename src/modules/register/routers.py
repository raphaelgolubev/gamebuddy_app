from fastapi import APIRouter
from .schemas import RegisterIn


router = APIRouter(prefix="/register", tags=["Регистрация"])


@router.post("/create")
async def create_user(user: RegisterIn):
    return user
