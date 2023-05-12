from fastapi import HTTPException, status

database_error = HTTPException(
    status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while working with database."
)
