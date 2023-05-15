from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Union


class RubricVariantCreate(BaseModel):
    rubric_id: int
    description: str


class RubricVariantShow(BaseModel):
    id: int
    rubric_id: int
    description: str

    class Config:
        orm_mode = True


class RubricVariantUpdate(BaseModel):
    rubric_id: int
    updated_description: str = Field(min_length=3)


class RecordCreate(BaseModel):
    title: str
    rubrics: List[RubricVariantCreate]
    patient_id: int

    @validator("rubrics", pre=True)
    def validate_rubrics(cls, value):
        prev = None
        for rubric in value:
            if prev == rubric["rubric_id"]:
                raise ValueError(
                    f"could not create more than one rubric variant with rubric_id {rubric['rubric_id']} for one record"
                )
            prev = rubric["rubric_id"]
        return value


class RecordShow(BaseModel):
    id: int
    title: str
    rubrics: List[RubricVariantShow]
    patient_id: int
    date: datetime

    class Config:
        orm_mode = True


class RecordUpdate(BaseModel):
    title: Union[str, None] = Field(min_length=3, default=None)
    rubrics: Union[List[RubricVariantUpdate], None]


class RecordDeleteResponse(BaseModel):
    deleted_record_id: int
