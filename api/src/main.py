from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .auth.router import auth_router
from .config import OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET
from .patients.router import patients_router
from .records.router import records_router
from .rubrics.router import rubrics_router

app = FastAPI(
    swagger_ui_init_oauth={
        "clientId": OAUTH2_CLIENT_ID,
        "clientSecret": OAUTH2_CLIENT_SECRET,
        "scopes": "email",
    },
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://disease-history.up.railway.app",
]

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
main_router.include_router(rubrics_router)


@main_router.get("/")
async def index():
    return RedirectResponse("/docs")


app.include_router(main_router)
