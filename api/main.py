from fastapi import FastAPI, APIRouter
from pydantic import EmailStr, BaseModel
from uvicorn import run
from typing import List, Union
from dal import DAL


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(TunedModel):
    email: EmailStr


class UserShow(TunedModel):
    some: Union[int, None] = None
    id: int
    email: EmailStr


class PatientShow(TunedModel):
    id: int
    full_name: str
    age: int
    diagnosis: str
    complaints: str
    anamnesis: str
    heredity: str
    treatment_comments: str


app = FastAPI()
main_router = APIRouter()


@main_router.post("/user", response_model=UserShow)
async def create_user(body: UserCreate) -> UserShow:
    new_user = await DAL.create_user(email=body.email)
    return UserShow.from_orm(new_user)


@main_router.get("/patients")
async def get_patients(user_id: int) -> List[PatientShow]:
    patients = await DAL.get_user_patients(user_id)
    return patients


app.include_router(main_router, tags=["routes"])

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
