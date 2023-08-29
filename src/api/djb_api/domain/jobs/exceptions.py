from fastapi import HTTPException


class Unauthorized(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=403, detail="Unauthorized")
