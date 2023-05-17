from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, PositiveInt, constr, validator

# Rubric Variants


class RubricVariantBase(BaseModel):
    rubric_id: PositiveInt
    description: constr(min_length=3)

    class Config:
        orm_mode = True


class RubricVariantsBase(BaseModel):
    __root__: List[RubricVariantBase]

    def __iter__(self):
        return iter(self.__root__)

    @validator("__root__")
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

    class Config:
        orm_mode = True


# Create
class RubricVariantCreate(RubricVariantBase):
    pass


class RubricVariantsCreate(RubricVariantsBase):
    __root__: List[RubricVariantCreate]


# Show
class RubricVariantShow(RubricVariantBase):
    id: PositiveInt


class RubricVariantsShow(RubricVariantsBase):
    __root__: List[RubricVariantShow]


# Update
class RubricVariantUpdate(RubricVariantBase):
    pass


class RubricVariantsUpdate(RubricVariantsBase):
    __root__: List[RubricVariantUpdate]


# Records


# Create
class RecordCreate(BaseModel):
    title: constr(min_length=3)
    rubrics: RubricVariantsCreate
    patient_id: PositiveInt


# Show
class RecordShow(BaseModel):
    id: PositiveInt
    title: constr(min_length=3)
    rubrics: List[RubricVariantShow]
    patient_id: PositiveInt
    date: datetime

    class Config:
        orm_mode = True


# Update
class RecordUpdate(BaseModel):
    title: Union[constr(min_length=3), None]
    rubrics: Union[RubricVariantsUpdate, None]


# Delete
class RecordDeleteResponse(BaseModel):
    deleted_record_id: PositiveInt
