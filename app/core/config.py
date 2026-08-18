import os
from dotenv import load_dotenv
load_dotenv()
# -----------------------------------
# JWT configuration
# -----------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")


ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "10"
    )
)


if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is not in .env"
    )