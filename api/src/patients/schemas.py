from typing import Union

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=3, default="Пациент")
    age: int = Field(ge=0, description="Age must be positive number", default=0)
    diagnosis: Union[str, None]
    complaints: Union[str, None]
    anamnesis: Union[str, None]
    heredity: Union[str, None]
    treatment_plan: Union[str, None]
    treatment_comments: Union[str, None]


class PatientShow(PatientCreate):
    class Config:
        orm_mode = True

    id: int
    user_id: int


class PatientUpdate(PatientCreate):
    full_name: Union[str, None] = Field(min_length=3, default=None)
    age: Union[int, None] = Field(
        ge=0, description="Age must be positive number", default=None
    )


class PatientDeleteResponse(BaseModel):
    deleted_patient_id: int
