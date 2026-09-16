"""
Custom application exceptions.

These exceptions represent expected application errors.
They do not create HTTP responses directly.
"""


class AppException(Exception):
    """Base exception for all application errors."""

    status_code = 500
    code = "INTERNAL_ERROR"
    message = "An unexpected error occurred."

    def __init__(
        self,
        message: str | None = None,
        details: dict | None = None,
    ):
        self.message = message or self.message
        self.details = details

        super().__init__(self.message)


class BadRequestException(AppException):
    """Raised when the request contains invalid business data."""

    status_code = 400
    code = "BAD_REQUEST"
    message = "Invalid request."


class UnauthorizedException(AppException):
    """Raised when authentication is required."""

    status_code = 401
    code = "UNAUTHORIZED"
    message = "Authentication required."


class ForbiddenException(AppException):
    """Raised when the user does not have permission."""

    status_code = 403
    code = "FORBIDDEN"
    message = "Permission denied."


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    status_code = 404
    code = "NOT_FOUND"
    message = "Resource not found."


class ConflictException(AppException):
    """Raised when the request conflicts with existing data."""

    status_code = 409
    code = "CONFLICT"
    message = "Resource conflict."


class InternalServerException(AppException):
    """Raised for known internal application failures."""

    status_code = 500
    code = "INTERNAL_ERROR"
    message = "Something went wrong."