from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from typing import List

from ..exceptions import DatabaseError

from .schemas import RubricSectionCreate, RubricCreate
from .models import RubricSection, Rubric
from .exceptions import RubricSectionNotFound, RubricNotFound


class RubricsService:
    @classmethod
    async def create_rubric_section(
        cls, section_data: RubricSectionCreate, db_session: AsyncSession
    ) -> RubricSection:
        try:
            async with db_session.begin():
                section = RubricSection(**section_data.dict())
                db_session.add(section)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return section

    @classmethod
    async def create_rubric(
        cls, rubric_data: RubricCreate, db_session: AsyncSession
    ) -> Rubric:
        rubric_section = cls.get_rubric_section(rubric_data.section_id, db_session)
        try:
            async with db_session.begin():
                rubric = Rubric(title=rubric_data.title, section=rubric_section)
                db_session.add(rubric)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return rubric

    @classmethod
    async def get_rubric_section(
        cls, section_id: int, db_session: AsyncSession
    ) -> RubricSection:
        try:
            async with db_session.begin():
                rubric_section = await db_session.get(RubricSection, section_id)
                if not rubric_section:
                    raise RubricSectionNotFound(section_id)
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return rubric_section

    @classmethod
    async def get_rubric(cls, rubric_id: int, db_session: AsyncSession) -> Rubric:
        try:
            async with db_session.begin():
                rubric = await db_session.get(Rubric, rubric_id)
                if not rubric:
                    raise RubricNotFound(rubric_id)
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        return rubric

    @classmethod
    async def get_rubrics_with_sections(
        cls, db_session: AsyncSession
    ) -> List[RubricSection]:
        try:
            async with db_session.begin():
                sections_with_rubrics = (
                    (
                        await db_session.scalars(
                            select(RubricSection).options(
                                joinedload(RubricSection.rubrics)
                            )
                        )
                    )
                    .unique()
                    .fetchall()
                )
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return sections_with_rubrics
