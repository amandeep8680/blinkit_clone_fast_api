from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.orm import Session

from  app.database.database import get_db
from  app.core.security import decode_token

from  app.models.admin_model import User
from  app.models.branchmanager_model import BranchManager
from  app.models.customer_model import Customer

from  app.constants import roles

from  app.exceptions.custom_exceptions import (
    UnauthorizedException,
)
from  app.exceptions import messages as msg


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Validate access token and return the
    authenticated user based on JWT role.
    """

    token = credentials.credentials
    payload = decode_token(token)

    # Only access tokens can access protected APIs.
    if payload.get("type") != "access":
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    unique_id = payload.get("sub")
    role = payload.get("role")

    if not unique_id or not role:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    # -----------------------------------
    # Super Admin
    # -----------------------------------
    if role == roles.SUPER_ADMIN:
        current_user = (
            db.query(User)
            .filter(
                User.unique_id == unique_id
            )
            .first()
        )

    # -----------------------------------
    # Branch Manager
    # -----------------------------------
    elif role == roles.BRANCH_MANAGER:
        current_user = (
            db.query(BranchManager)
            .filter(
                BranchManager.unique_id == unique_id
            )
            .first()
        )

    # -----------------------------------
    # Customer
    # -----------------------------------
    elif role == roles.CUSTOMER:
        current_user = (
            db.query(Customer)
            .filter(
                Customer.unique_id == unique_id
            )
            .first()
        )

    else:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    # Token user no longer exists.
    if not current_user:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    # Block inactive users.
    if not current_user.is_active:
        raise UnauthorizedException(
            msg.USER_INACTIVE
        )

    # Ensure JWT role still matches DB role.
    if current_user.role != role:
        raise UnauthorizedException(
            msg.INVALID_TOKEN
        )

    return current_user