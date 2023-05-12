from pydantic import BaseModel
from datetime import datetime
from typing import List


class RubricVariantCreate(BaseModel):
    rubric_id: int
    description: str


class RubricVariantShow(BaseModel):
    id: int
    rubric_id: int
    description: str

    class Config:
        orm_mode = True


class RecordCreate(BaseModel):
    title: str
    rubrics: List[RubricVariantCreate]
    patient_id: int


class RecordShow(BaseModel):
    id: int
    title: str
    rubrics: List[RubricVariantShow]
    patient_id: int
    date: datetime

    class Config:
        orm_mode = True
