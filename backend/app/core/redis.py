# app/core/redis.py

import redis

from app.core.config import REDIS_URL


# =========================================================
# Redis Client
# =========================================================

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


# =========================================================
# Test Redis Connection
# =========================================================

def check_redis_connection() -> bool:
    """
    Check whether FastAPI can connect
    to the Redis server.
    """

    try:
        return redis_client.ping()

    except redis.RedisError:
        return False