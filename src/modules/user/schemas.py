from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: UUID
    role: str
    email: EmailStr
    password: str
    is_activated: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
