import logging
import os

from dotenv import load_dotenv

from app.core.redis import redis_client


load_dotenv()

logger = logging.getLogger("app")


MAX_FAILED_ATTEMPTS = int(
    os.getenv("MAX_FAILED_ATTEMPTS", "5")
)

BLOCK_TIME_SECONDS = int(
    os.getenv("BLOCK_TIME_SECONDS", "60")
)


def get_login_attempt_key(
    ip: str,
    email: str,
):
    return f"login:fail:{ip}:{email.lower()}"


def is_login_blocked(
    ip: str,
    email: str,
):
    key = get_login_attempt_key(
        ip=ip,
        email=email,
    )

    attempts = redis_client.get(key)

    if attempts is None:
        return False

    if int(attempts) >= MAX_FAILED_ATTEMPTS:
        logger.warning(
            "LOGIN BLOCKED | ip=%s | email=%s | attempts=%s",
            ip,
            email,
            attempts,
        )

        return True

    return False


def record_failed_login(
    ip: str,
    email: str,
):
    key = get_login_attempt_key(
        ip=ip,
        email=email,
    )

    attempts = redis_client.incr(key)

    if attempts == 1:
        redis_client.expire(
            key,
            BLOCK_TIME_SECONDS,
        )

    logger.warning(
        "FAILED LOGIN | ip=%s | email=%s | attempts=%s",
        ip,
        email,
        attempts,
    )

    return attempts


def reset_failed_logins(
    ip: str,
    email: str,
):
    key = get_login_attempt_key(
        ip=ip,
        email=email,
    )

    redis_client.delete(key)

    logger.info(
        "LOGIN ATTEMPTS RESET | ip=%s | email=%s",
        ip,
        email,
    )