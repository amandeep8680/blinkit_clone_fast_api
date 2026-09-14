import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("app")


def error_response(
    *,
    status_code: int,
    message: str,
    request_id: str,
) -> JSONResponse:
    """
    Build a standard error response.
    """

    response_data = {
        "success": False,
        "detail": message,
        "request_id": request_id,
    }

    response = JSONResponse(
        status_code=status_code,
        content=response_data,
    )

    response.headers["X-Request-ID"] = request_id

    return response


async def logging_middleware(
    request: Request,
    call_next,
):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "API REQUEST | request_id=%s | method=%s | "
            "path=%s | status=%s | duration_ms=%.2f | client_ip=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request.client.host
            if request.client
            else "unknown",
        )

        return response

    except Exception as exc:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        # Only truly unexpected exceptions reach here.
        # Full traceback is logged.
        logger.exception(
            "API UNEXPECTED ERROR | request_id=%s | method=%s | "
            "path=%s | error_type=%s | error=%s | "
            "duration_ms=%.2f | client_ip=%s",
            request_id,
            request.method,
            request.url.path,
            type(exc).__name__,
            str(exc),
            duration_ms,
            request.client.host
            if request.client
            else "unknown",
        )

        return error_response(
            status_code=500,
            message="Internal server error",
            request_id=request_id,
        )