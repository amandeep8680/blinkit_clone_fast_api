from passlib.context import CryptContext
from datetime import datetime , timedelta , timezone
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from  app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from  app.exceptions.custom_exceptions import (
    UnauthorizedException,
)

from  app.exceptions import messages as msg

# -----------------------------------
# Password hashing configuration
# -----------------------------------

pwd_context  = CryptContext(
    schemes=['bcrypt'],
    deprecated = "auto"
)

def hash_password(password : str) ->str:
    ''' Function to convert plain password into hash password'''

    return pwd_context.hash(password)


def verify_password(plain_password : str , hashed_password : str ) -> bool:
    return pwd_context.verify(
        plain_password, hashed_password
    )





# -----------------------------------
# JWT configuration
# -----------------------------------

def create_access_token(
        unique_id:str,
        role:str
) ->str:
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub":unique_id,
        "role":role,
        "type":"access",
        "exp": expire
    }

    token = jwt.encode(
        payload , 
        SECRET_KEY ,
        algorithm=ALGORITHM
    )

    return token




def create_refresh_token(
    unique_id: str,
    role:str
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    payload = {
        "sub": unique_id,
        "type": "refresh",
        "role":role,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token




def decode_token(token:str) ->dict:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except ExpiredSignatureError:
        raise UnauthorizedException(
            msg.TOKEN_EXPIRED
        )

    except InvalidTokenError:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )