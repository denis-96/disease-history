import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.auth.schemas import UserSchema
from src.auth.service import AuthService
from src.config import TEST_DATABASE_URL
from src.database import Base, get_db
from src.main import app
from src.models import User
from src.rubrics.schemas import RubricCreate, RubricSectionCreate
from src.rubrics.service import RubricsService

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = async_session()
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(autouse=True, scope="session")
async def prepare_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as db_session:
        section_id = (
            await RubricsService.create_rubric_sections(
                [RubricSectionCreate(title="Пищеварительная система")], db_session
            )
        )[0].id
        await RubricsService.create_rubrics(
            [
                RubricCreate(section_id=section_id, title="Желудок"),
                RubricCreate(section_id=section_id, title="Пищевод"),
            ],
            db_session,
        )
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
async def user():
    async with async_session() as db_session:
        yield await AuthService.register_new_user(
            UserSchema(id=1, email="user@gmail.com"), db_session
        )
    async with async_session() as db_session, db_session.begin():
        await db_session.execute(delete(User).where(User.email == "user@gmail.com"))


@pytest.fixture(scope="module")
async def another_user():
    async with async_session() as db_session:
        yield await AuthService.register_new_user(
            UserSchema(id=2, email="another.user@gmail.com"), db_session
        )
    async with async_session() as db_session, db_session.begin():
        await db_session.execute(
            delete(User).where(User.email == "another.user@gmail.com")
        )
