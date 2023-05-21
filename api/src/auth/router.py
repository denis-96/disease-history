from typing import Annotated, Union

from fastapi import APIRouter, Cookie, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .dependencies import (
    get_current_user,
    get_refresh_token,
    get_user_from_refresh_token,
)
from .models import RefreshToken
from .schemas import (
    AccessToken,
    AuthSchema,
    CheckAuthResponse,
    TokenRequest,
    UserSchema,
)
from .service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("")
async def auth(
    auth_data: AuthSchema,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
    old_refresh_token: Annotated[
        Union[str, None], Cookie(..., alias="refreshToken")
    ] = None,
) -> AccessToken:
    if old_refresh_token:
        await AuthService.expire_refresh_token(old_refresh_token, db_session)

    auth_tokens = await AuthService.authenticate_user(
        auth_data=auth_data, db_session=db_session
    )
    response.set_cookie(
        **AuthService.generate_refresh_token_cookie(auth_tokens.refresh_token).dict(
            exclude_none=True
        )
    )
    return AccessToken(access_token=auth_tokens.access_token)


@auth_router.post("/token")
async def token(
    grant_type: Annotated[str, Form()],
    code: Annotated[str, Form()],
    client_id: Annotated[str, Form()],
    client_secret: Annotated[str, Form()],
    redirect_uri: Annotated[str, Form()],
    db_session: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
    old_refresh_token: Annotated[
        Union[str, None], Cookie(..., alias="refreshToken")
    ] = None,
) -> AccessToken:
    token_params = TokenRequest(
        grant_type=grant_type,
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    google_id_token = await AuthService.get_google_id_token(token_params)

    return await auth(
        AuthSchema(google_id_token=google_id_token.id_token),
        db_session,
        response,
        old_refresh_token,
    )


@auth_router.get("/token/refresh")
async def refresh_token(
    user: Annotated[UserSchema, Depends(get_user_from_refresh_token)],
) -> AccessToken:
    new_access_token = AuthService.generate_token(UserSchema.from_orm(user))
    return AccessToken(access_token=new_access_token)


@auth_router.get("/logout")
async def logout(
    refresh_token: Annotated[RefreshToken, Depends(get_refresh_token)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
) -> None:
    await AuthService.expire_refresh_token(refresh_token, db_session)
    response.delete_cookie(
        **AuthService.generate_refresh_token_cookie(
            refresh_token.refresh_token, expired=True
        ).dict(exclude_none=True)
    )


@auth_router.get("/check")
async def check_auth(
    user: Annotated[UserSchema, Depends(get_current_user)]
) -> CheckAuthResponse:
    return CheckAuthResponse(authenticated=True, user=user)
