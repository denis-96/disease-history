from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import OAUTH2_AUTH_URL
from ..database import get_db
from ..models import User
from .schemas import Token, UserSchema
from .service import AuthService

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=OAUTH2_AUTH_URL,
    tokenUrl="/auth/token",
)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
    return AuthService.verify_token(Token(access_token=token))


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
