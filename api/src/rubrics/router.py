from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user_id
from ..config import ADMIN_ID
from ..database import get_db
from .exceptions import NotAdmin
from .schemas import (
    RubricCreate,
    RubricSectionCreate,
    RubricSectionShow,
    RubricShow,
    SectionWithRubrics,
)
from .service import RubricsService

rubrics_router = APIRouter(prefix="/rubric", tags=["Rubrics"])


@rubrics_router.post("/section")
async def create_rubric_sections(
    section_data: List[RubricSectionCreate],
    user_id: Annotated[int, Depends(get_current_user_id)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> List[RubricSectionShow]:
    if user_id != ADMIN_ID:
        raise NotAdmin

    return await RubricsService.create_rubric_sections(section_data, db_session)


@rubrics_router.post("")
async def create_rubrics(
    rubric_data: List[RubricCreate],
    user_id: Annotated[int, Depends(get_current_user_id)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> List[RubricShow]:
    if user_id != ADMIN_ID:
        raise NotAdmin

    return await RubricsService.create_rubrics(rubric_data, db_session)


@rubrics_router.get("/section")
async def get_rubric_section(
    section_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> RubricSectionShow:
    return await RubricsService.get_rubric_section(section_id, db_session)


@rubrics_router.get("")
async def get_rubric(
    rubric_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> RubricShow:
    return await RubricsService.get_rubric(rubric_id, db_session)


@rubrics_router.get("/all")
async def get_sections_with_rubrics(
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> List[SectionWithRubrics]:
    return await RubricsService.get_rubrics_with_sections(db_session)
