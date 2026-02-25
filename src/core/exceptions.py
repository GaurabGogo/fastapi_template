from typing import Any


class AppException(Exception):
    """Base exception for the application."""
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        errors: dict[str, Any] | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationException(AppException):
    def __init__(self, errors: dict[str, Any], message: str = "Validation failed"):
        super().__init__(message, status_code=422, errors=errors)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)
