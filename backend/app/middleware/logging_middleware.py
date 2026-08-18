import time
import logging

from fastapi import Request


logger = logging.getLogger("app")


async def logging_middleware(
    request: Request,
    call_next
):
    start_time = time.perf_counter()

    # Request aayi
    logger.info(
        "Request | method=%s | path=%s",
        request.method,
        request.url.path
    )

    # Request ko actual API ki taraf bhejo
    response = await call_next(request)

    # API complete
    process_time = (
        time.perf_counter() - start_time
    )

    # Response log karo
    logger.info(
        "Response | status=%s | time=%.3fs",
        response.status_code,
        process_time
    )

    return response