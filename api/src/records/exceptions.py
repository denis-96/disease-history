from fastapi import HTTPException, status


class RubricNotFound(HTTPException):
    def __init__(self, rubric_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rubric with id {rubric_id} does not exist.",
        )


class RecordNotFound(HTTPException):
    def __init__(self, record_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Treatments record with id {record_id} does not exist.",
        )


class RecordAccessDenied(HTTPException):
    def __init__(self, record_id):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have access to the treatment record with id {record_id}.",
        )
