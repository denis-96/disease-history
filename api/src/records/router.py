from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from ..database import get_db
from ..auth.dependencies import get_current_user_id
from ..patients.dependencies import get_patient
from ..patients.models import Patient

from .models import TreatmentRecord
from .schemas import RecordCreate, RecordShow
from .service import RecordsService
from .dependencies import get_record

records_router = APIRouter(prefix="/record", tags=["Records"])


@records_router.get("")
async def get_one_record(
    record: Annotated[TreatmentRecord, Depends(get_record)]
) -> RecordShow:
    return record


@records_router.get("/all")
async def get_patient_records(
    patient: Annotated[Patient, Depends(get_patient)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> List[RecordShow]:
    return await RecordsService.get_patient_records(patient, db_session)


@records_router.post("")
async def create_record(
    record_data: RecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> RecordShow:
    return await RecordsService.create_record(record_data, user_id, db_session)


@records_router.patch("")
async def create_record():
    pass


@records_router.delete("")
async def create_record():
    pass
