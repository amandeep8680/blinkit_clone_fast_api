from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import decode_token
from app.models.admin_model import User

from app.exceptions.custom_exceptions import UnauthorizedException
from app.exceptions import messages as msg


# Defines Bearer token authentication for protected APIs.
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Validates the Bearer access token and returns
    the currently authenticated user.
    """

    # Extract the JWT from: Authorization: Bearer <token>
    token = credentials.credentials

    # Decode and validate the JWT.
    payload = decode_token(token)

    # Only access tokens can be used for protected APIs.
    if payload.get("type") != "access":
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    # Get the user's unique ID from the token.
    unique_id = payload.get("sub")
    role = payload.get("role")

    if not unique_id:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    # Find the authenticated user in the database.
    user = (
        db.query(User)
        .filter(User.unique_id == unique_id)
        .first()
    )

    if not user:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    # Prevent inactive users from accessing APIs.
    if not user.is_active:
        raise UnauthorizedException(
            msg.SUPER_ADMIN_INACTIVE
        )
    
    if user.role != role:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        ) 
    return user