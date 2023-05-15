from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from ..database import get_db
from ..auth.dependencies import get_current_user_id
from ..patients.dependencies import get_patient
from ..patients.models import Patient

from .models import TreatmentRecord
from .schemas import (
    RecordCreate,
    RecordShow,
    RecordUpdate,
    RecordDeleteResponse,
    RubricVariantCreate,
    RubricVariantShow,
)
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
async def update_record(
    updated_record_params: RecordUpdate,
    record: Annotated[TreatmentRecord, Depends(get_record)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> RecordShow:
    return await RecordsService.update_record(updated_record_params, record, db_session)


@records_router.delete("")
async def delete_record(
    record: Annotated[TreatmentRecord, Depends(get_record)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> RecordDeleteResponse:
    return await RecordsService.delete_record(record, db_session)


@records_router.post("/rubric-variants")
async def create_rubric_variants(
    rubric_variants_data: List[RubricVariantCreate],
    record: Annotated[TreatmentRecord, Depends(get_record)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> List[RubricVariantShow]:
    return await RecordsService.create_rubric_variants(
        rubric_variants_data, record, db_session
    )
