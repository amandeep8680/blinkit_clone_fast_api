import json
import redis
from app.core.redis import redis_client
import logging 

## everycache is implemented in the categores services
## get active categories....


logger = logging.getLogger("app")

def get_cache(key: str):
    """
    Get cached data from Redis.

    Returns:
        Python data if cache exists.
        None if cache does not exist.
    """
    try:
        cached_data = redis_client.get(key)

        if not cached_data:
            return None

        return json.loads(cached_data)
    except redis.RedisError as e:
        logger.warning(
            "CACHE READ FAILED | key=%s | error=%s",
            key,
            str(e),
        )

        return None

def set_cache(
    key: str,
    data,
    ttl: int = 60,
):
    try:
        redis_client.set(
            key,
            json.dumps(data),
            ex=ttl,
        )

        logger.info(
            "CACHE SET | key=%s | ttl=%s",
            key,
            ttl,
        )

    except redis.RedisError as e:
        logger.warning(
            "CACHE WRITE FAILED | key=%s | error=%s",
            key,
            str(e),
        )

def delete_cache(key: str):
    """
    Delete a specific cache key.

    Used when database data changes
    and old cache becomes stale.
    """
    try:
        redis_client.delete(key)
    except redis.RedisError as e:
        logger.info(
            " CACHE DELETE FAILED | "
            "key=%s | error=%s"
        )


def delete_cache_pattern(pattern: str):
    try:
        keys = list(
            redis_client.scan_iter(
                match=pattern
            )
        )

        if keys:
            redis_client.delete(*keys)

            logger.info(
                "CACHE INVALIDATED | pattern=%s | deleted_keys=%s",
                pattern,
                len(keys),
            )

    except redis.RedisError as e:
        logger.warning(
            "CACHE INVALIDATION FAILED | pattern=%s | error=%s",
            pattern,
            str(e),
        )




## reusable helper function

def get_or_set_cache(
    key: str,
    fetch_function,
    ttl: int = 60,
):
    """
    Get data from cache.

    If cache miss happens:
    - call fetch_function()
    - store result in cache
    - return result
    """

    cached_data = get_cache(key)

    if cached_data is not None:
        logger.info(
            "CACHE HIT | key=%s")
        return cached_data

    logger.info(
        "CACHE MISS | key=%s",
        key,
    )


    data = fetch_function()

    set_cache(
        key=key,
        data=data,
        ttl=ttl,
    )

    return data


