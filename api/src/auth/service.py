from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from requests import post as post_request
from datetime import datetime, timedelta
from typing import Union
import jwt


from ..config import SECRET_KEY, JWT_ALGORITHM, CLIENT_ID
from ..models import User
from .schemas import (
    UserSchema,
    Token,
    TokenRequest,
    GoogleIdToken,
    GoogleUser,
    AuthSchema,
)


class AuthService:
    @classmethod
    def verify_token(cls, token: Token) -> UserSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token.access_token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            exception.detail = "Token has been expired"
            raise exception from None
        except jwt.InvalidSignatureError:
            exception.detail = "Invalid token"
            raise exception from None

        user_data = payload.get("user")
        try:
            user = UserSchema(id=user_data.get("id"), email=user_data.get("email"))
        except ValidationError:
            raise exception

        return user

    @classmethod
    def generate_token(cls, user: UserSchema, expires_minutes: int = 30) -> Token:
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=expires_minutes),
            "sub": str(user.id),
            "user": user.dict(),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )
        return Token(access_token=token)

    @classmethod
    def verify_google_id_token(cls, token: str) -> GoogleUser:
        try:
            id_info = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
            user = GoogleUser(
                id=id_info["sub"],
                email=id_info["email"],
                email_verified=id_info["email_verified"],
            )
        except (ValueError, KeyError):
            raise HTTPException(403, "Bad code")
        return user

    @classmethod
    def get_google_id_token(cls, params: TokenRequest) -> Union[GoogleIdToken, None]:
        response = post_request(
            "https://oauth2.googleapis.com/token",
            data=params.dict(),
        )
        if response.status_code == 200:
            token_data = response.json()
            id_token = token_data.get("id_token")
            if id_token:
                return GoogleIdToken(id_token=id_token)
        raise HTTPException(403, "Bad token parameters")

    @classmethod
    async def register_new_user(cls, user_data: UserSchema, db_session: AsyncSession):
        async with db_session.begin():
            user = User(
                email=user_data.email,
            )
            db_session.add(user)
            await db_session.flush()

        token = cls.generate_token(UserSchema.from_orm(user))
        return Token(access_token=token.access_token)

    @classmethod
    async def authenticate_user(
        cls, auth_data: AuthSchema, db_session: AsyncSession
    ) -> Token:
        user_data = AuthService.verify_google_id_token(auth_data.google_id_token)

        async with db_session.begin():
            user = await db_session.scalar(
                select(User).filter_by(email=user_data.email)
            )

        if user:
            token = cls.generate_token(UserSchema.from_orm(user))
            return Token(access_token=token.access_token)

        return await cls.register_new_user(user_data, db_session)
