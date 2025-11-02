from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, resource: str, resource_id: int | str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found",
        )


class ConflictError(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)
