from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..exceptions import DatabaseError
from ..patients.service import PatientsService
from ..patients.models import Patient
from ..rubrics.service import RubricsService

from .schemas import (
    RecordCreate,
    RecordUpdate,
    RubricVariantCreate,
    RubricVariantUpdate,
    RecordDeleteResponse,
)
from .models import TreatmentRecord, RubricVariant
from .exceptions import RecordNotFound, RecordAccessDenied


class RecordsService:
    @classmethod
    async def create_record(
        cls, record_data: RecordCreate, user_id: int, db_session: AsyncSession
    ) -> TreatmentRecord:
        patient = await PatientsService.get_patient(
            record_data.patient_id, user_id, db_session
        )
        try:
            async with db_session.begin():
                record = TreatmentRecord(title=record_data.title, patient=patient)
                db_session.add(record)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        await cls.create_rubric_variants(record_data.rubrics, record, db_session)
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
            raise DatabaseError()

        return record

    @classmethod
    async def get_patient_records(
        cls, patient: Patient, db_session: AsyncSession
    ) -> List[TreatmentRecord]:
        try:
            async with db_session.begin():
                records = await patient.awaitable_attrs.treatment_records
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return records

    @classmethod
    async def delete_record(
        cls, record: TreatmentRecord, db_session: AsyncSession
    ) -> RecordDeleteResponse:
        record_id = record.id
        try:
            async with db_session.begin():
                await db_session.delete(record)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return RecordDeleteResponse(deleted_record_id=record_id)

    @classmethod
    async def update_record(
        cls,
        updated_record_params: RecordUpdate,
        record: TreatmentRecord,
        db_session: AsyncSession,
    ) -> TreatmentRecord:
        try:
            async with db_session.begin():
                params_dict = updated_record_params.dict(
                    exclude_none=True, exclude={"rubrics"}
                )
                for param in params_dict:
                    setattr(record, param, params_dict[param])
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return record

    @classmethod
    async def create_rubric_variants(
        cls,
        rubric_variants_data: List[RubricVariantCreate],
        record: TreatmentRecord,
        db_session: AsyncSession,
    ) -> List[RubricVariant]:
        rubric_variants = [
            RubricVariant(
                description=variant.description,
                rubric=await RubricsService.get_rubric(variant.rubric_id, db_session),
            )
            for variant in rubric_variants_data
        ]
        try:
            async with db_session.begin():
                (await record.awaitable_attrs.rubrics).extend(rubric_variants)
                await db_session.flush()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise DatabaseError()
        return rubric_variants

    @classmethod
    async def update_rubric_variants(
        cls,
        updated_rubric_variants: List[RubricVariantUpdate],
        record: TreatmentRecord,
        db_session: AsyncSession,
    ) -> List[RubricVariant]:
        pass
