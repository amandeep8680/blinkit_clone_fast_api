"""
Middleware for managing Request-ID for each HTTP request.
"""

import uuid

from fastapi import Request, Response


def get_or_create_request_id(request: Request) -> str:
    """Get Request-ID from header or create a new one."""
    return (
        request.headers.get("X-Request-ID")
        or str(uuid.uuid4())
    )


def set_request_id(
    request: Request,
    request_id: str,
) -> None:
    """Store Request-ID for the current request."""
    request.state.request_id = request_id


def add_request_id_to_response(
    response: Response,
    request_id: str,
) -> None:
    """Add Request-ID to the response header."""
    response.headers["X-Request-ID"] = request_id


async def request_middleware(
    request: Request,
    call_next,
):
    """
    Manage Request-ID lifecycle:
    create/get → store → process request → add to response.
    """

    # Get existing Request-ID or create a new one
    request_id = get_or_create_request_id(request)

    # Store it so other parts of the app can access it
    set_request_id(request, request_id)

    # Continue request processing
    response = await call_next(request)

    # Send the same Request-ID back to the client
    add_request_id_to_response(
        response,
        request_id,
    )

    return response