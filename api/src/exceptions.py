from typing import List

from fastapi import HTTPException, status


class ValidationHTTPException(HTTPException):
    def __init__(self, status_code: int, loc: List[str], msg: str, type: str):
        super().__init__(
            status_code=status_code,
            detail=[
                {
                    "loc": loc,
                    "msg": msg,
                    "type": type,
                }
            ],
        )


class DatabaseError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while working with database.",
        )
