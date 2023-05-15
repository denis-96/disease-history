from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .dependencies import get_current_user
from .schemas import AuthSchema, CheckAuthResponse, Token, TokenRequest, UserSchema
from .service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("")
async def auth(
    auth_data: AuthSchema, db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    return await AuthService.authenticate_user(
        auth_data=auth_data, db_session=db_session
    )


@auth_router.post("/token")
async def token(
    grant_type: Annotated[str, Form()],
    code: Annotated[str, Form()],
    client_id: Annotated[str, Form()],
    client_secret: Annotated[str, Form()],
    redirect_uri: Annotated[str, Form()],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    token_params = TokenRequest(
        grant_type=grant_type,
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    try:
        google_id_token = await AuthService.get_google_id_token(token_params)
    except ValidationError:
        raise HTTPException(400, detail="Invalid data")
    return await AuthService.authenticate_user(
        AuthSchema(google_id_token=google_id_token.id_token), db_session
    )


@auth_router.get("/check")
async def check_auth(
    user: Annotated[UserSchema, Depends(get_current_user)]
) -> CheckAuthResponse:
    return CheckAuthResponse(authenticated=True, user=user)
