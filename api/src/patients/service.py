from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..models import User
from ..exceptions import DatabaseError

from .models import Patient
from .schemas import PatientCreate, PatientUpdate, PatientDeleteResponse
from .exceptions import PatientAccessDenied, PatientNotFound


class PatientsService:
    @classmethod
    async def create_patient(
        cls, patient_data: PatientCreate, user_id: int, db_session: AsyncSession
    ) -> Patient:
        try:
            async with db_session.begin():
                patient = Patient(**patient_data.dict(), user_id=user_id)
                db_session.add(patient)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return patient

    @classmethod
    async def get_patient(
        cls, patient_id: int, user_id: int, db_session: AsyncSession
    ) -> Patient:
        try:
            async with db_session.begin():
                patient = await db_session.get(Patient, patient_id)
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        if not patient:
            raise PatientNotFound(patient_id)
        if patient.user_id != user_id:
            raise PatientAccessDenied(patient_id)

        return patient

    @classmethod
    async def get_patients(cls, user: User, db_session) -> List[Patient]:
        try:
            async with db_session.begin():
                patients = await user.awaitable_attrs.patients
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return patients

    @classmethod
    async def delete_patient(
        cls, patient: Patient, db_session: AsyncSession
    ) -> PatientDeleteResponse:
        patient_id = patient.id
        try:
            async with db_session.begin():
                await db_session.delete(patient)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return PatientDeleteResponse(deleted_patient_id=patient_id)

    @classmethod
    async def update_patient(
        cls,
        updated_patient_params: PatientUpdate,
        patient: Patient,
        db_session: AsyncSession,
    ) -> Patient:
        try:
            async with db_session.begin():
                params_dict = updated_patient_params.dict(exclude_none=True)
                for param in params_dict:
                    setattr(patient, param, params_dict[param])
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return patient
