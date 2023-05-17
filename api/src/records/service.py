from typing import List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import DatabaseError
from ..patients.models import Patient
from ..patients.service import PatientsService
from ..rubrics.service import RubricsService
from .exceptions import RecordAccessDenied, RecordNotFound
from .models import RubricVariant, TreatmentRecord
from .schemas import (
    RecordCreate,
    RecordDeleteResponse,
    RecordUpdate,
    RubricVariantsCreate,
    RubricVariantsUpdate,
)


class RecordsService:
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

        await cls._create_rubric_variants(record_data.rubrics, record, db_session)
        return record

    @classmethod
    async def update_record(
        cls,
        updated_record_params: RecordUpdate,
        record: TreatmentRecord,
        db_session: AsyncSession,
    ) -> TreatmentRecord:
        try:
            async with db_session.begin():
                updated_record_params.title and setattr(
                    record, "title", updated_record_params.title
                )
                await db_session.flush()

        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        updated_record_params.rubrics and await cls._update_rubric_variants(
            updated_record_params.rubrics, record, db_session
        )

        return record

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
    async def _create_rubric_variants(
        cls,
        rubric_variants_data: RubricVariantsCreate,
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
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return rubric_variants

    @classmethod
    async def _update_rubric_variants(
        cls,
        updated_rubric_variants: RubricVariantsUpdate,
        record: TreatmentRecord,
        db_session: AsyncSession,
    ) -> List[RubricVariant]:
        uncreated_variants = []
        try:
            async with db_session.begin():
                for variant in updated_rubric_variants:
                    rubric_variant = await db_session.scalar(
                        select(RubricVariant).filter_by(
                            rubric_id=variant.rubric_id, record=record
                        )
                    )
                    if rubric_variant:
                        rubric_variant.description = variant.description
                        await db_session.flush()
                    else:
                        uncreated_variants.append(variant)
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return await cls._create_rubric_variants(uncreated_variants, record, db_session)
