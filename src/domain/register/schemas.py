from uuid import UUID
from pydantic import BaseModel, EmailStr


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


class RegisterOut(BaseModel):
    id: UUID
