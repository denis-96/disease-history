from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List

from ..patients.service import PatientsService
from ..exceptions import database_error
from .schemas import RecordCreate
from .models import TreatmentRecord, RubricVariant, Rubric
from .exceptions import RubricNotFound, RecordNotFound, RecordAccessDenied


class RecordsService:
    @classmethod
    async def create_record(
        cls, record_data: RecordCreate, user_id: int, db_session: AsyncSession
    ) -> TreatmentRecord:
        patient = await PatientsService.get_patient(
            record_data.patient_id, user_id, db_session
        )
        record_rubrics = [
            RubricVariant(
                description=rubric.description,
                rubric=await cls.get_rubric(rubric.rubric_id, db_session),
            )
            for rubric in record_data.rubrics
        ]
        try:
            async with db_session.begin():
                record = TreatmentRecord(
                    title=record_data.title, patient=patient, rubrics=record_rubrics
                )
                db_session.add(record)
                await db_session.flush()
        except IntegrityError:
            await db_session.rollback()
            raise RubricNotFound()
        except SQLAlchemyError:
            await db_session.rollback()
            raise database_error

        return record

    @classmethod
    async def get_record(
        cls, record_id: int, user_id: int, db_session: AsyncSession
    ) -> TreatmentRecord:
        try:
            async with db_session.begin():
                record = await db_session.get(TreatmentRecord, record_id)
                if not record:
                    raise RecordNotFound(record_id)
                if (await record.awaitable_attrs.patient).user_id != user_id:
                    raise RecordAccessDenied(record_id)
        except SQLAlchemyError:
            await db_session.rollback()
            raise database_error

        return record

    @classmethod
    async def get_patient_records(cls, patient, db_session) -> List[TreatmentRecord]:
        try:
            async with db_session.begin():
                records = await patient.awaitable_attrs.treatment_records
        except SQLAlchemyError:
            await db_session.rollback()
            raise database_error
        return records

    @classmethod
    async def get_rubric(cls, rubric_id: int, db_session: AsyncSession):
        try:
            async with db_session.begin():
                rubric = await db_session.get(Rubric, rubric_id)
        except SQLAlchemyError:
            await db_session.rollback()
            raise database_error
        if not rubric:
            raise RubricNotFound(rubric_id)
        return rubric
