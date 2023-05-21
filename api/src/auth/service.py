from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Union

import jwt
from cryptography.x509 import load_pem_x509_certificate
from httpx import AsyncClient, codes
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import (
    JWT_ALGORITHM,
    JWT_REFRESH_TOKEN_EXP,
    JWT_TOKEN_EXP,
    OAUTH2_CERTS_URL,
    OAUTH2_CLIENT_ID,
    OAUTH2_TOKEN_URL,
    SECRET_KEY,
)
from ..exceptions import DatabaseError
from ..models import User
from .exceptions import (
    CertsFetchingError,
    ExpiredToken,
    InvalidCredentianls,
    InvalidGoogleToken,
    InvalidParamsForToken,
    InvalidToken,
)
from .models import RefreshToken
from .schemas import (
    AuthSchema,
    AuthTokens,
    GoogleIdToken,
    GoogleUser,
    RefreshTokenCookie,
    TokenRequest,
    UserSchema,
)


class AuthService:
    @classmethod
    def verify_token(cls, token: str) -> UserSchema:
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )

        except jwt.ExpiredSignatureError:
            raise ExpiredToken()
        except (jwt.InvalidSignatureError, jwt.DecodeError):
            raise InvalidToken()
        user_data = payload.get("user")
        try:
            user = UserSchema(id=user_data.get("id"), email=user_data.get("email"))
        except ValidationError:
            raise InvalidCredentianls()

        return user

    @classmethod
    def generate_token(
        cls, user: UserSchema, expire_seconds: int = JWT_TOKEN_EXP
    ) -> str:
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=expire_seconds),
            "sub": str(user.id),
            "user": user.dict(),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )
        return token

    @classmethod
    def generate_refresh_token_cookie(
        cls,
        refresh_token: str,
        expired: bool = False,
    ) -> RefreshTokenCookie:
        if expired:
            return RefreshTokenCookie()

        return RefreshTokenCookie(value=refresh_token, max_age=JWT_REFRESH_TOKEN_EXP)

    @classmethod
    async def create_refresh_token(cls, user: User, db_session: AsyncSession) -> str:
        try:
            async with db_session.begin():
                refresh_token = RefreshToken(
                    refresh_token=token_urlsafe(),
                    expires_at=datetime.utcnow()
                    + timedelta(seconds=JWT_REFRESH_TOKEN_EXP),
                )
                (await user.awaitable_attrs.refresh_tokens).append(refresh_token)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return refresh_token.refresh_token

    @classmethod
    async def get_refresh_token(
        cls, refresh_token: str, db_session: AsyncSession
    ) -> RefreshToken:
        try:
            async with db_session.begin():
                refresh_token = await db_session.scalar(
                    select(RefreshToken).filter_by(refresh_token=refresh_token)
                )
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return refresh_token

    @classmethod
    async def expire_refresh_token(
        cls, refresh_token: Union[str, RefreshToken], db_session: AsyncSession
    ) -> None:
        if type(refresh_token) == str:
            db_refresh_token = await cls.get_refresh_token(refresh_token, db_session)
        else:
            db_refresh_token = refresh_token
        try:
            async with db_session.begin():
                if db_refresh_token:
                    db_refresh_token.expires_at = datetime.utcnow() - timedelta(days=1)
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

    @classmethod
    async def create_auth_tokens(
        cls, user: User, db_session: AsyncSession
    ) -> AuthTokens:
        access_token = cls.generate_token(UserSchema.from_orm(user))
        refresh_token = await cls.create_refresh_token(user, db_session)
        return AuthTokens(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    async def verify_google_id_token(cls, token: str) -> GoogleUser:
        async with AsyncClient() as client:
            certs_response = await client.get(OAUTH2_CERTS_URL)
            if certs_response.status_code != codes.OK:
                raise CertsFetchingError()
            certs = certs_response.json()
        try:
            token_header = jwt.get_unverified_header(token)
            print(token_header)
            token_key = load_pem_x509_certificate(
                bytes(certs[token_header["kid"]], encoding="utf-8")
            ).public_key()
            id_info = jwt.decode(
                token,
                key=token_key,
                algorithms=[token_header["alg"]],
                audience=OAUTH2_CLIENT_ID,
            )
            print(id_info)
            user = GoogleUser(
                id=id_info["sub"],
                email=id_info["email"],
                email_verified=id_info["email_verified"],
            )
        except (
            jwt.PyJWTError,
            KeyError,
            ValueError,
        ) as e:
            print(e)
            raise InvalidGoogleToken()
        return user

    @classmethod
    async def get_google_id_token(
        cls, params: TokenRequest
    ) -> Union[GoogleIdToken, None]:
        async with AsyncClient() as client:
            response = await client.post(
                OAUTH2_TOKEN_URL,
                data=params.dict(),
            )
        print(response.json())
        if response.status_code == codes.OK:
            token_data = response.json()
            id_token = token_data.get("id_token")
            if id_token:
                return GoogleIdToken(id_token=id_token)
        raise InvalidParamsForToken()

    @classmethod
    async def register_new_user(
        cls, user_data: UserSchema, db_session: AsyncSession
    ) -> AuthTokens:
        try:
            async with db_session.begin():
                user = User(
                    email=user_data.email,
                )
                db_session.add(user)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return await cls.create_auth_tokens(user, db_session)

    @classmethod
    async def authenticate_user(
        cls, auth_data: AuthSchema, db_session: AsyncSession
    ) -> AuthTokens:
        user_data = await AuthService.verify_google_id_token(auth_data.google_id_token)
        try:
            async with db_session.begin():
                user = await db_session.scalar(
                    select(User).filter_by(email=user_data.email)
                )
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        if user:
            return await cls.create_auth_tokens(user, db_session)

        return await cls.register_new_user(user_data, db_session)
