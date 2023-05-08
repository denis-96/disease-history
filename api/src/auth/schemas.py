from pydantic import BaseModel, EmailStr
from typing import Union


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    id: Union[int, None] = None
    email: EmailStr


class Token(BaseModel):
    access_token: str


class BearerToken(Token):
    token_type: str = "bearer"
