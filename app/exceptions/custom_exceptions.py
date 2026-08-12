# app/exceptions/custom_exceptions.py

from fastapi import HTTPException, status


class AppException(HTTPException):
    """
    Base exception for application HTTP errors.
    """

    def __init__(
        self,
        status_code: int,
        detail: str
    ):
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class BadRequestException(AppException):
    """
    400 - Request data or operation is invalid.
    """

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class UnauthorizedException(AppException):
    """
    401 - User is not authenticated.
    """

    def __init__(
        self,
        message: str = "Authentication required."
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )


class ForbiddenException(AppException):
    """
    403 - User is authenticated but does not
    have permission to access the resource.
    """

    def __init__(
        self,
        message: str = "Permission denied."
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class NotFoundException(AppException):
    """
    404 - Requested resource does not exist.
    """

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )


class ConflictException(AppException):
    """
    409 - Resource already exists or request
    conflicts with current state.
    """

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class InternalServerException(AppException):
    """
    500 - Unexpected server-side error.
    """

    def __init__(
        self,
        message: str = "Something went wrong."
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )