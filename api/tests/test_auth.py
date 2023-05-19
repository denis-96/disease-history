from httpx import AsyncClient, codes


async def test_token(client: AsyncClient):
    response = await client.get("/auth/check")
    assert response.status_code == codes.UNAUTHORIZED
