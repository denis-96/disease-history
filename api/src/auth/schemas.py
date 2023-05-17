from typing import Union

from pydantic import AnyHttpUrl, BaseModel, EmailStr


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


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenCookie(BaseModel):
    key: str = "refreshToken"
    httponly: bool = True
    samesite: str = "none"
    secure: bool = True
    value: Union[str, None]
    max_age: Union[int, None]


class GoogleIdToken(BaseModel):
    id_token: str


class TokenRequest(BaseModel):
    grant_type: str
    code: str
    client_id: str
    client_secret: str
    redirect_uri: AnyHttpUrl
