from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user_id
from ..database import get_db
from .models import Patient
from .service import PatientsService


async def get_patient(
    patient_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> Patient:
    patient = await PatientsService.get_patient(
        patient_id=patient_id, user_id=user_id, db_session=db_session
    )
    return patient
