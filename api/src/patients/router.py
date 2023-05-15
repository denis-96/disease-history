from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_db_user, get_current_user_id
from ..database import get_db
from ..models import User
from .dependencies import get_patient
from .models import Patient
from .schemas import PatientCreate, PatientDeleteResponse, PatientShow, PatientUpdate
from .service import PatientsService

patients_router = APIRouter(prefix="/patient", tags=["Patients"])


@patients_router.get("", description="Get patient")
async def get_one_patient(
    patient: Annotated[Patient, Depends(get_patient)]
) -> PatientShow:
    return patient


@patients_router.get("/all", description="Get patients")
async def get_all_patients(
    user: Annotated[User, Depends(get_current_db_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> List[PatientShow]:
    return await PatientsService.get_patients(user=user, db_session=db_session)


@patients_router.post("", description="Create patient")
async def create_patient(
    patient_data: PatientCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> PatientShow:
    return await PatientsService.create_patient(
        patient_data=patient_data, user_id=user_id, db_session=db_session
    )


@patients_router.patch("")
async def update_patient(
    updated_patient_params: PatientUpdate,
    patient: Annotated[Patient, Depends(get_patient)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> PatientShow:
    return await PatientsService.update_patient(
        updated_patient_params, patient, db_session
    )


@patients_router.delete("")
async def delete_patient(
    patient: Annotated[Patient, Depends(get_patient)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> PatientDeleteResponse:
    return await PatientsService.delete_patient(patient, db_session)
