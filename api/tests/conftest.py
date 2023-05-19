import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import TEST_DATABASE_URL
from src.database import get_db
from src.main import app

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = async_session()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(autouse=True, scope="session")
def run_migrations() -> None:
    import os

    print("running migrations..")
    os.system("alembic upgrade head")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
