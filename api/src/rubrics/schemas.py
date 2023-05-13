from pydantic import BaseModel
from typing import List


class RubricSectionCreate(BaseModel):
    title: str


class RubricSectionShow(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class RubricCreate(BaseModel):
    section_id: int
    title: str


class RubricShow(BaseModel):
    id: int
    section_id: int
    title: str

    class Config:
        orm_mode = True


class SectionWithRubrics(BaseModel):
    id: int
    title: str
    rubrics: List[RubricShow]

    class Config:
        orm_mode = True
