from fastapi import Depends
from app.auth.dependencies import get_current_user
from app.exceptions.custom_exceptions import ForbiddenException
from app.exceptions import messages as msg


def require_roles(*allowed_roles: str):

    def role_checker(
        current_user=Depends(get_current_user)
    ):
        
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                msg.FORBIDDEN
            )

        return current_user

    return role_checker