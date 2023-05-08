from fastapi import HTTPException, status
from pydantic import ValidationError, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from os.path import join as join_path
import jwt

from ..config import SECRET_KEY, JWT_ALGORITHM, SERVER_HOST, SERVER_PORT, BASE_DIR
from ..utils import send_email
from ..models import User
from .schemas import UserSchema, Token, BearerToken


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
        except jwt.InvalidKeyError:
            raise exception from None

        user_data = payload.get("user")

        try:
            user = UserSchema.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def generate_token(cls, user: UserSchema) -> Token:
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(),
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
    def send_auth_email(cls, recipient_email: EmailStr):
        token = AuthService.generate_token(UserSchema(email=recipient_email))
        auth_link = (
            f"http://{SERVER_HOST}:{SERVER_PORT}/auth?token={token.access_token}"
        )

        subject = "Авторизация"
        plain_message = f'Перейдите по ссылке для асторизации на сайте "История болезни"\n{auth_link}'
        html_message = ""
        with open(join_path(BASE_DIR, "emails", "auth_email.html")) as file:
            html_message = file.read().replace("auth_link", auth_link)

        send_email(recipient_email, subject, plain_message, html_message)

    @classmethod
    async def register_new_user(cls, user_data: UserSchema, db_session: AsyncSession):
        async with db_session.begin():
            user = User(
                email=user_data.email,
            )
            db_session.add(user)
            await db_session.flush()

        token = cls.generate_token(UserSchema.from_orm(user))
        return BearerToken(access_token=token.access_token)

    @classmethod
    async def authenticate_user(
        cls, auth_token: Token, db_session: AsyncSession
    ) -> BearerToken:
        user_data = cls.verify_token(auth_token)

        if user_data.id:
            async with db_session.begin():
                user = await db_session.get(User, user.id)

            if user:
                token = cls.generate_token(UserSchema.from_orm(user))
                return BearerToken(access_token=token.access_token)

        return await cls.register_new_user(user_data, db_session)
