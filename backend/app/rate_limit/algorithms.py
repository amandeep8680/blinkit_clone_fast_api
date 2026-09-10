import time
import uuid

from app.core.redis import redis_client


# =========================================================
# FIXED WINDOW
# =========================================================

async def fixed_window(
    key: str,
    limit: int,
    window_seconds: int,
):
    current = redis_client.incr(key)

    ttl = redis_client.ttl(key)

    if current == 1 or ttl == -1:
        redis_client.expire(key, window_seconds)

    ttl = redis_client.ttl(key)

    if current > limit:
        return False, ttl

    return True, ttl


# =========================================================
# TOKEN BUCKET
# =========================================================

async def token_bucket(
    key: str,
    capacity: int,
    refill_rate: float,
):
    now = time.time()

    data = redis_client.hgetall(key)

    if not data:
        tokens = float(capacity)
        last_refill = now
    else:
        tokens = float(data.get("tokens", capacity))
        last_refill = float(data.get("last_refill", now))

    elapsed = now - last_refill

    tokens_to_add = elapsed * refill_rate

    tokens = min(
        capacity,
        tokens + tokens_to_add,
    )

    if tokens < 1:
        allowed = False
    else:
        tokens -= 1
        allowed = True

    redis_client.hset(
        key,
        mapping={
            "tokens": tokens,
            "last_refill": now,
        },
    )

    ttl = max(
        60,
        int((capacity / refill_rate) * 2),
    )

    redis_client.expire(key, ttl)

    if allowed:
        retry_after = 0
    else:
        retry_after = max(
            1,
            int((1 - tokens) / refill_rate) + 1,
        )

    return allowed, retry_after


# =========================================================
# SLIDING WINDOW
# =========================================================

async def sliding_window(
    key: str,
    limit: int,
    window_seconds: int,
):
    now = time.time()

    # Window ki starting time
    window_start = now - window_seconds

    # Purani requests remove karo
    redis_client.zremrangebyscore(
        key,
        0,
        window_start,
    )

    # Current window me kitni requests hain
    current_requests = redis_client.zcard(key)

    # Limit already reach ho chuki hai
    if current_requests >= limit:
        oldest = redis_client.zrange(
            key,
            0,
            0,
            withscores=True,
        )

        if oldest:
            oldest_timestamp = oldest[0][1]

            retry_after = max(
                1,
                int(
                    oldest_timestamp
                    + window_seconds
                    - now
                )
                + 1,
            )
        else:
            retry_after = 1

        return False, retry_after

    # Har request ka unique member
    request_id = f"{now}:{uuid.uuid4()}"

    # Current request add karo
    redis_client.zadd(
        key,
        {
            request_id: now
        },
    )

    # Redis cleanup
    redis_client.expire(
        key,
        window_seconds,
    )

    return True, 0


# =========================================================
# LEAKY BUCKET
# =========================================================

async def leaky_bucket(
    key: str,
    capacity: int,
    leak_rate: float,
):
    """
    capacity:
        Queue/bucket maximum kitni requests hold karega.

    leak_rate:
        Har second kitni requests bucket se process/remove hongi.

    Example:
        capacity = 10
        leak_rate = 2

        Maximum 10 pending requests.
        Har second 2 requests leak/process hongi.
    """

    now = time.time()

    data = redis_client.hgetall(key)

    if not data:
        water = 0.0
        last_leak = now
    else:
        water = float(
            data.get("water", 0)
        )

        last_leak = float(
            data.get("last_leak", now)
        )

    # Last check ke baad kitna time pass hua
    elapsed = now - last_leak

    # Itne requests bucket se leak/process ho chuke honge
    leaked = elapsed * leak_rate

    water = max(
        0,
        water - leaked,
    )

    # Bucket full hai
    if water + 1 > capacity:
        allowed = False

        retry_after = max(
            1,
            int(
                (water + 1 - capacity)
                / leak_rate
            )
            + 1,
        )

    else:
        # Current request bucket me add karo
        water += 1

        allowed = True
        retry_after = 0

    redis_client.hset(
        key,
        mapping={
            "water": water,
            "last_leak": now,
        },
    )

    ttl = max(
        60,
        int((capacity / leak_rate) * 2),
    )

    redis_client.expire(
        key,
        ttl,
    )

    return allowed, retry_after