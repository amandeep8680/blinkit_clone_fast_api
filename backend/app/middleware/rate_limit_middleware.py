from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.routing import Match

from app.rate_limit.policies import RATE_LIMIT_POLICIES
from app.rate_limit.algorithms import (
    fixed_window,
    sliding_window,
    token_bucket,
    leaky_bucket,
)

def get_route_path(request: Request):
    for route in request.app.routes:
        match, _ = route.matches(request.scope)

        if match == Match.FULL:
            return getattr(
                route,
                "path",
                request.url.path,
            )

    return request.url.path


def get_policy(method: str, path: str):
    for policy in RATE_LIMIT_POLICIES.values():
        if (method, path) in policy.get("routes", []):
            return policy

    return None


async def rate_limit_middleware(request: Request, call_next):
    method = request.method.upper()
    path = get_route_path(request)

    policy = get_policy(method, path)

    if not policy:
        return await call_next(request)

    algorithm = policy["algorithm"]
    client_ip = request.client.host if request.client else "unknown"

    key = f"rl:{algorithm}:{method}:{path}:{client_ip}"

    if algorithm == "fixed_window":
        allowed, retry_after = await fixed_window(
            key,
            policy["limit"],
            policy["window_seconds"],
        )

    elif algorithm == "sliding_window":
        allowed, retry_after = await sliding_window(
            key,
            policy["limit"],
            policy["window_seconds"],
        )

    elif algorithm == "token_bucket":
        allowed, retry_after = await token_bucket(
            key,
            policy["capacity"],
            policy["refill_rate"],
        )

    elif algorithm == "leaky_bucket":
        allowed, retry_after = await leaky_bucket(
            key,
            policy["capacity"],
            policy["leak_rate"],
        )

    else:
        return await call_next(request)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
            headers={"Retry-After": str(max(retry_after, 1))},
        )

    return await call_next(request)