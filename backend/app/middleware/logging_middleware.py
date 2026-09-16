"""
Middleware for logging HTTP requests and unexpected errors.
"""

import logging
import time

from fastapi import Request


logger = logging.getLogger("app")


def get_request_context(request: Request) -> dict:
    """Return common request information used in logs."""
    return {
        "request_id": getattr(
            request.state,
            "request_id",
            None,
        ),
        "method": request.method,
        "path": request.url.path,
        "client_ip": (
            request.client.host
            if request.client
            else "unknown"
        ),
    }


def get_duration_ms(start_time: float) -> float:
    """Return request execution time in milliseconds."""
    return (
        time.perf_counter() - start_time
    ) * 1000


def get_log_level(status_code: int) -> int:
    """Return log level according to HTTP status code."""
    if status_code >= 500:
        return logging.ERROR

    if status_code >= 400:
        return logging.WARNING

    return logging.INFO


def log_request(
    *,
    request: Request,
    status_code: int,
    duration_ms: float,
) -> None:
    """Log a completed HTTP request."""

    context = get_request_context(request)

    log_data = {
        **context,
        "status_code": status_code,
        "duration_ms": duration_ms,
    }

    message = (
        "API REQUEST | "
        "request_id=%(request_id)s | "
        "method=%(method)s | "
        "path=%(path)s | "
        "status=%(status_code)s | "
        "duration_ms=%(duration_ms).2f | "
        "client_ip=%(client_ip)s"
    )

    log_level = get_log_level(status_code)

    logger.log(
        log_level,
        message,
        log_data,
    )


def log_unexpected_error(
    *,
    request: Request,
    exc: Exception,
    duration_ms: float,
) -> None:
    """Log an unexpected exception with its traceback."""

    context = get_request_context(request)

    log_data = {
        **context,
        "error_type": type(exc).__name__,
        "error": str(exc),
        "duration_ms": duration_ms,
    }

    # logger.exception automatically includes traceback
    logger.exception(
        "API UNEXPECTED ERROR | "
        "request_id=%(request_id)s | "
        "method=%(method)s | "
        "path=%(path)s | "
        "error_type=%(error_type)s | "
        "error=%(error)s | "
        "duration_ms=%(duration_ms).2f | "
        "client_ip=%(client_ip)s",
        log_data,
    )


async def logging_middleware(
    request: Request,
    call_next,
):
    """
    Measure request time and log completed requests
    or unexpected errors.
    """

    # Start request timer
    start_time = time.perf_counter()

    try:
        # Continue request processing
        response = await call_next(request)

    except Exception as exc:
        duration_ms = get_duration_ms(start_time)

        # Log error with traceback
        log_unexpected_error(
            request=request,
            exc=exc,
            duration_ms=duration_ms,
        )

        # Re-raise the same exception
        raise

    # Calculate total request time
    duration_ms = get_duration_ms(start_time)

    # Log completed request
    log_request(
        request=request,
        status_code=response.status_code,
        duration_ms=duration_ms,
    )

    return response