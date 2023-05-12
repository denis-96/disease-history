from fastapi import HTTPException, status

patient_access_denied = HTTPException(
    status.HTTP_403_FORBIDDEN,
    detail="You do not have access to the patient with this id.",
)

patient_not_found = HTTPException(
    status.HTTP_404_NOT_FOUND, detail="Patient with this id does not exist."
)
