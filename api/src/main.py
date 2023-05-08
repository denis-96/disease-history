from fastapi import FastAPI, APIRouter
from uvicorn import run

from .auth.router import auth_router

app = FastAPI()

main_router = APIRouter()
main_router.include_router(auth_router)

app.include_router(main_router)

# class TunedModel(BaseModel):
#     class Config:
#         orm_mode = True


# class UserShow(TunedModel):
#     id: int
#     email: EmailStr


# class PatientShow(TunedModel):
#     id: int
#     full_name: str
#     age: int
#     diagnosis: str
#     complaints: str
#     anamnesis: str
#     heredity: str
#     treatment_comments: str


# # @main_router.post("/user", response_model=UserShow)
# # async def create_user(body: UserCreate) -> UserShow:
# #     new_user = await DAL.create_user(email=body.email)
# #     return UserShow.from_orm(new_user)


# @app.get("/patients")
# async def get_patients(user_id: int) -> List[PatientShow]:
#     patients = await DAL.get_user_patients(user_id)
#     return patients


# @app.get("/login")
# async def login(token: str):
#     return token_manager.verify_token(token)


if __name__ == "__main__":
    run(app, host="192.168.0.10", port=5000)
