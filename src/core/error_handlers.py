import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import AppException
from src.core.responses import send_response

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException):
    return send_response(
        success=False,
        message=exc.message,
        errors=exc.errors,
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        loc = error["loc"]
        field = ".".join(str(item) for item in loc[1:]) if len(loc) > 1 else loc[0]
        errors[field] = error["msg"]

    return send_response(
        success=False,
        message="Validation Error",
        errors=errors,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return send_response(
        success=False,
        message=exc.detail,
        status_code=exc.status_code,
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return send_response(
        success=False,
        message="Internal Server Error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_error_handlers(app):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
