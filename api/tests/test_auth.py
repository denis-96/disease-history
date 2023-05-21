from httpx import AsyncClient, codes

from src.auth.schemas import AuthTokens, UserSchema
from src.auth.service import AuthService


def test_tokens():
    user = UserSchema(id=2321, email="test@email.com")
    token = AuthService.generate_token(user)
    token_data = AuthService.verify_token(token)
    assert user == token_data


async def test_auth(client: AsyncClient, user: AuthTokens):
    response = await client.get(
        "/auth/check", headers={"Authorization": f"Bearer {user.access_token}"}
    )
    json = response.json()
    assert response.status_code == codes.OK
    assert json["authenticated"] == True
    assert json["user"]["email"] == "user@gmail.com"


async def test_expired_token(client: AsyncClient):
    expired_token = AuthService.generate_token(
        UserSchema(id=1, email="user@gmail.com"), -100
    )
    response = await client.get(
        "/auth/check", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == codes.UNAUTHORIZED


async def test_good_refresh_token(client: AsyncClient, user: AuthTokens):
    token_response = await client.get(
        "/auth/token/refresh", cookies={"refreshToken": user.refresh_token}
    )
    response = await client.get(
        "/auth/check",
        headers={"Authorization": f"Bearer {token_response.json()['access_token']}"},
    )
    assert response.status_code == codes.OK


async def test_invalid_refresh_token(client: AsyncClient):
    res = await client.get(
        "/auth/token/refresh", cookies={"refreshToken": "invalid refresh token"}
    )
    assert res.status_code == codes.UNAUTHORIZED
    assert res.json()["detail"] == "Invalid refresh token"


async def test_logout(client: AsyncClient, user: AuthTokens):
    res = await client.get("/auth/logout", cookies={"refreshToken": user.refresh_token})
    assert res.status_code == codes.OK


async def test_refresh_when_logged_out(client: AsyncClient, user: AuthTokens):
    res = await client.get(
        "/auth/token/refresh", cookies={"refreshToken": user.refresh_token}
    )
    assert res.status_code == codes.UNAUTHORIZED
    assert res.json()["detail"] == "Refresh token has been expired"
