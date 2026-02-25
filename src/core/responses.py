from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None
    meta: dict[str, Any] | None = None
    errors: Any | None = None
    status_code: int


def send_response(
    message: str,
    data: Any = None,
    meta: dict[str, Any] | None = None,
    errors: Any = None,
    success: bool = True,
    status_code: int = 200,
    cookies: dict[str, str] | None = None,
    **kwargs
) -> JSONResponse:
    """
    Standardizes API response format and handles cookies.
    """
    response_data = ApiResponse(
        success=success,
        message=message,
        data=data,
        meta=meta,
        errors=errors,
        status_code=status_code
    )

    # Use jsonable_encoder to handle complex types like datetimes
    content = jsonable_encoder(response_data)

    response = JSONResponse(
        status_code=status_code,
        content=content,
        **kwargs
    )

    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key=key, value=value, httponly=True)

    return response
