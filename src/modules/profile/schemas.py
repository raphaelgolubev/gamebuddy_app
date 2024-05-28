from uuid import UUID
from pydantic import BaseModel


class ProfileSchema(BaseModel):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
