from fastapi import HTTPException, status
from ..exceptions import ValidationHTTPException


class NotAdmin(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permissions to do this.",
        )


class RubricSectionNotFound(ValidationHTTPException):
    def __init__(self, section_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            loc=["section_id"],
            msg=f"rubric section with id {section_id} does not exist",
            type="not found",
        )


class RubricNotFound(ValidationHTTPException):
    def __init__(self, rubric_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            loc=["rubric_id"],
            msg=f"rubric with id {rubric_id} does not exist",
            type="not found",
        )
