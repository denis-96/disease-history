from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .auth.router import auth_router
from .patients.router import patients_router
from .records.router import records_router

from .config import CLIENT_ID, CLIENT_SECRET

app = FastAPI(
    swagger_ui_init_oauth={
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "scopes": "email",
    },
)

origins = ["http://localhost", "http://localhost:3000", "http://192.168.0.10:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(patients_router)
main_router.include_router(records_router)


@main_router.get("/")
async def index():
    return RedirectResponse("/docs")


app.include_router(main_router)
