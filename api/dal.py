from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from models import User, Patient, async_session


class DAL:
    @staticmethod
    async def create_user(email: EmailStr) -> User:
        async with async_session() as session:
            async with session.begin():
                try:
                    new_user = User(email=email)
                    session.add(new_user)
                    await session.flush()
                    return new_user
                except IntegrityError:
                    raise HTTPException(
                        status_code=422, detail="User with such email already exists"
                    )

    @staticmethod
    async def get_user_patients(user_id) -> Patient:
        async with async_session() as session:
            async with session.begin():
                user: User = await session.query(User).filter_by(id=user_id).first()
                if user:
                    return user.patients.all()
