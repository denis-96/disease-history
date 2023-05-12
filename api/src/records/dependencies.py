from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..database import get_db
from ..auth.dependencies import get_current_user_id

from .models import TreatmentRecord
from .service import RecordsService


async def get_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> TreatmentRecord:
    return await RecordsService.get_record(record_id, user_id, db_session)
