from uuid import UUID
from pydantic import BaseModel, EmailStr
from core.database import Base
from modules.user.schemas import UserSchema


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


class RegisterOut(BaseModel):
    id: UUID
