import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("app")


async def logging_middleware(
    request: Request,
    call_next,
):
    # Unique ID for this request
    request_id = str(uuid.uuid4())

    # Store request ID inside the current request.
    # Downstream routes/services that receive Request
    # can access the same ID using:
    # request.state.request_id
    # request-specific data temporarily store karne ki jagah deta hai.
    request.state.request_id = request_id

    # Start timer before API execution
    start_time = time.perf_counter()

    try:
        # Send request to next middleware / API
        response = await call_next(request)

        # Calculate total request processing time
        duration = time.perf_counter() - start_time

        # Convert seconds into milliseconds
        duration_ms = duration * 1000

        # Log successful request information
        logger.info(
            "API REQUEST | request_id=%s | method=%s | "
            "path=%s | status=%s | duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response

    except Exception as e:

        # Calculate duration even when request fails
        duration = time.perf_counter() - start_time
        duration_ms = duration * 1000

        # logger.exception automatically includes traceback
        logger.exception(
            "API ERROR | request_id=%s | method=%s | path=%s | "
            "error_type=%s | error=%s | duration_ms=%.2f | client_ip=%s",
            request_id,
            request.method,
            request.url.path,
            type(e).__name__,
            str(e),
            duration_ms,
            request.client.host if request.client else "unknown",
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id,
            },
        )