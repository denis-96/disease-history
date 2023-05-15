from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field, validator

# Rubric Variants


# Create
class RubricVariantCreate(BaseModel):
    rubric_id: int
    description: str = Field(min_length=3)


class RubricVariantsCreate(BaseModel):
    __root__: List[RubricVariantCreate]

    def __iter__(self):
        return iter(self.__root__)

    @validator("__root__", pre=True)
    def validate_rubrics(cls, value):
        print(value)
        prev = None
        for rubric in value:
            if prev == rubric["rubric_id"]:
                raise ValueError(
                    f"could not have more than one rubric variant with rubric_id {rubric['rubric_id']} for one record"
                )
            prev = rubric["rubric_id"]
        return value


# Show
class RubricVariantShow(BaseModel):
    id: int
    rubric_id: int
    description: str

    class Config:
        orm_mode = True


class RubricVariantsShow(BaseModel):
    __root__: List[RubricVariantShow]

    def __iter__(self):
        return iter(self.__root__)

    class Config:
        orm_mode = True


# Update
class RubricVariantUpdate(RubricVariantCreate):
    pass


class RubricVariantsUpdate(RubricVariantsCreate):
    __root__: List[RubricVariantUpdate]


# Records


# Create
class RecordCreate(BaseModel):
    title: str
    rubrics: RubricVariantsCreate
    patient_id: int


# Show
class RecordShow(BaseModel):
    id: int
    title: str
    rubrics: List[RubricVariantShow]
    patient_id: int
    date: datetime

    class Config:
        orm_mode = True


# Update
class RecordUpdate(BaseModel):
    title: Union[str, None] = Field(min_length=3, default=None)
    rubrics: Union[RubricVariantsUpdate, None]


# Delete
class RecordDeleteResponse(BaseModel):
    deleted_record_id: int
