from pydantic import BaseModel
from typing import Any, List, Optional


class ErrorDetail(BaseModel):
    field: str
    message: str


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[ErrorDetail]] = None


def success_response(message: str = "Success", data: Any = None) -> dict:
    """Create a standardized success response."""
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }


def error_response(message: str = "Error", errors: Optional[List[dict]] = None) -> dict:
    """Create a standardized error response."""
    error_list = None
    if errors:
        error_list = [ErrorDetail(**e) for e in errors]

    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": error_list
    }
