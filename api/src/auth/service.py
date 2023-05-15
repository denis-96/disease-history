from datetime import datetime, timedelta
from typing import Union

import jwt
from cryptography.x509 import load_pem_x509_certificate
from httpx import AsyncClient, codes
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import (
    JWT_ALGORITHM,
    OAUTH2_CERTS_URL,
    OAUTH2_CLIENT_ID,
    OAUTH2_TOKEN_URL,
    SECRET_KEY,
)
from ..models import User
from .exceptions import (
    CertsFetchingError,
    ExpiredToken,
    InvalidCredentianls,
    InvalidGoogleToken,
    InvalidParamsForToken,
    InvalidToken,
)
from .schemas import (
    AuthSchema,
    GoogleIdToken,
    GoogleUser,
    Token,
    TokenRequest,
    UserSchema,
)


class AuthService:
    @classmethod
    def verify_token(cls, token: Token) -> UserSchema:
        try:
            payload = jwt.decode(
                token.access_token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise InvalidToken()
        except jwt.InvalidSignatureError:
            raise ExpiredToken()
        user_data = payload.get("user")
        try:
            user = UserSchema(id=user_data.get("id"), email=user_data.get("email"))
        except ValidationError:
            raise InvalidCredentianls()

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
    async def verify_google_id_token(cls, token: str) -> GoogleUser:
        async with AsyncClient() as client:
            certs_response = await client.get(OAUTH2_CERTS_URL)
            if certs_response.status_code != codes.OK:
                raise CertsFetchingError()
            certs = certs_response.json()
        try:
            token_header = jwt.get_unverified_header(token)
            token_key = load_pem_x509_certificate(
                bytes(certs[token_header["kid"]], encoding="utf-8")
            ).public_key()
            id_info = jwt.decode(
                token,
                key=token_key,
                algorithms=[token_header["alg"]],
                audience=OAUTH2_CLIENT_ID,
            )
            user = GoogleUser(
                id=id_info["sub"],
                email=id_info["email"],
                email_verified=id_info["email_verified"],
            )
        except (
            jwt.PyJWTError,
            KeyError,
            ValueError,
        ):
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
        if response.status_code == codes.OK:
            token_data = response.json()
            id_token = token_data.get("id_token")
            if id_token:
                return GoogleIdToken(id_token=id_token)
        raise InvalidParamsForToken()

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
        user_data = await AuthService.verify_google_id_token(auth_data.google_id_token)

        async with db_session.begin():
            user = await db_session.scalar(
                select(User).filter_by(email=user_data.email)
            )

        if user:
            token = cls.generate_token(UserSchema.from_orm(user))
            return Token(access_token=token.access_token)

        return await cls.register_new_user(user_data, db_session)
