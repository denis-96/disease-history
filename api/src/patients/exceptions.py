from fastapi import HTTPException, status

from ..exceptions import ValidationHTTPException


class PatientNotFound(ValidationHTTPException):
    def __init__(self, patient_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            loc=["patient_id"],
            msg=f"patient with this id {patient_id} does not exist",
            type="not found",
        )


class PatientAccessDenied(HTTPException):
    def __init__(self, patient_id):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have access to the patient with id {patient_id}",
        )
