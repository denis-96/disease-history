from typing import List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..exceptions import DatabaseError
from .exceptions import RubricNotFound, RubricSectionNotFound
from .models import Rubric, RubricSection
from .schemas import RubricCreate, RubricSectionCreate


class RubricsService:
    @classmethod
    async def create_rubric_sections(
        cls, sections_data: List[RubricSectionCreate], db_session: AsyncSession
    ) -> List[RubricSection]:
        sections = [RubricSection(**section.dict()) for section in sections_data]
        try:
            async with db_session.begin():
                db_session.add_all(sections)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return sections

    @classmethod
    async def create_rubrics(
        cls, rubrics_data: List[RubricCreate], db_session: AsyncSession
    ) -> List[Rubric]:
        sections = set((rubric.section_id for rubric in rubrics_data))
        [
            await cls.get_rubric_section(section_id, db_session)
            for section_id in sections
        ]
        rubrics = [
            Rubric(
                title=rubric.title,
                section_id=rubric.section_id,
            )
            for rubric in rubrics_data
        ]
        try:
            async with db_session.begin():
                db_session.add_all(rubrics)
                await db_session.flush()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return rubrics

    @classmethod
    async def get_rubric_section(
        cls, section_id: int, db_session: AsyncSession
    ) -> RubricSection:
        try:
            async with db_session.begin():
                rubric_section = await db_session.get(RubricSection, section_id)
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        if not rubric_section:
            raise RubricSectionNotFound(section_id)
        return rubric_section

    @classmethod
    async def get_rubric(cls, rubric_id: int, db_session: AsyncSession) -> Rubric:
        try:
            async with db_session.begin():
                rubric = await db_session.get(Rubric, rubric_id)

        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()
        if not rubric:
            raise RubricNotFound(rubric_id)
        return rubric

    @classmethod
    async def get_rubrics_with_sections(
        cls, db_session: AsyncSession
    ) -> List[RubricSection]:
        try:
            async with db_session.begin():
                sections_with_rubrics = await db_session.scalars(
                    select(RubricSection).options(joinedload(RubricSection.rubrics))
                )
                sections_with_rubrics = sections_with_rubrics.unique().fetchall()
        except SQLAlchemyError:
            await db_session.rollback()
            raise DatabaseError()

        return sections_with_rubrics
