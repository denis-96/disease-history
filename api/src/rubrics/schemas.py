from typing import List

from pydantic import BaseModel, PositiveInt, constr


class RubricSectionCreate(BaseModel):
    title: constr(min_length=3)


class RubricSectionShow(BaseModel):
    id: PositiveInt
    title: constr(min_length=3)

    class Config:
        orm_mode = True


class RubricCreate(BaseModel):
    section_id: PositiveInt
    title: constr(min_length=3)


class RubricShow(BaseModel):
    id: PositiveInt
    section_id: PositiveInt
    title: constr(min_length=3)

    class Config:
        orm_mode = True


class SectionWithRubrics(BaseModel):
    id: PositiveInt
    title: constr(min_length=3)
    rubrics: List[RubricShow]

    class Config:
        orm_mode = True
