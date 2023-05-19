from datetime import datetime
from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import OAUTH2_AUTH_URL
from ..database import get_db
from ..exceptions import DatabaseError
from ..models import User
from .exceptions import ExpiredRefreshToken, InvalidRefreshToken
from .models import RefreshToken
from .schemas import UserSchema
from .service import AuthService

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=OAUTH2_AUTH_URL,
    tokenUrl="/auth/token",
    refreshUrl="/auth/token/refresh",
)


def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)]
) -> UserSchema:
    return AuthService.verify_token(access_token)


def get_current_user_id(
    user_data: Annotated[UserSchema, Depends(get_current_user)]
) -> int:
    return user_data.id


async def get_current_db_user(
    user_data: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    async with db_session.begin():
        return await db_session.get(User, user_data.id)


async def get_refresh_token(
    refresh_token: Annotated[str, Cookie(..., alias="refreshToken")],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> RefreshToken:
    db_refresh_token = await AuthService.get_refresh_token(refresh_token, db_session)
    if not db_refresh_token:
        raise InvalidRefreshToken()

    if not datetime.utcnow() <= db_refresh_token.expires_at:
        raise ExpiredRefreshToken()
    return db_refresh_token


async def get_user_from_refresh_token(
    refresh_token: Annotated[RefreshToken, Depends(get_refresh_token)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    try:
        async with db_session.begin():
            user = await refresh_token.awaitable_attrs.user
    except SQLAlchemyError:
        await db_session.rollback()
        raise DatabaseError()
    return user
