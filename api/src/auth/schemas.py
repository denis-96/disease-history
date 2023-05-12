from pydantic import BaseModel, EmailStr, AnyHttpUrl


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    id: int
    email: EmailStr


class GoogleUser(BaseModel):
    id: int
    email: EmailStr
    email_verified: bool


class CheckAuthResponse(BaseModel):
    authenticated: bool
    user: UserSchema


class AuthSchema(BaseModel):
    google_id_token: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GoogleIdToken(BaseModel):
    id_token: str


class TokenRequest(BaseModel):
    grant_type: str
    code: str
    client_id: str
    client_secret: str
    redirect_uri: AnyHttpUrl
