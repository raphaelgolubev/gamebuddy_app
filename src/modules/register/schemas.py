from pydantic import BaseModel


class RegisterIn(BaseModel):
    email: str
    password: str
