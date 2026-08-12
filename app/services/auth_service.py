from sqlalchemy.orm import Session

from app.models.usermodel import User
from app.schemas.auth_schema import LoginRequest

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

from app.exceptions.custom_exceptions import UnauthorizedException
from app.exceptions import messages as msg


class AuthService:

    def login(
        self,
        db: Session,
        credentials: LoginRequest
    ):
        user = (
            db.query(User)
            .filter(User.email == credentials.email)
            .first()
        )

        if not user:
            raise UnauthorizedException(
                msg.INVALID_CREDENTIALS
            )

        if not verify_password(
            credentials.password,
            user.password_hash
        ):
            raise UnauthorizedException(
                msg.INVALID_CREDENTIALS
            )

        if not user.is_active:
            raise UnauthorizedException(
                msg.SUPER_ADMIN_INACTIVE
            )

        access_token = create_access_token(
            user.unique_id
        )

        refresh_token = create_refresh_token(
            user.unique_id
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }




    def refresh_access_token(
            self, 
            db:Session,
            refresh_token:str
    ):
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise UnauthorizedException(
                msg.INVALID_TOKEN
            )
        unique_id = payload.get("sub")
        
        if not unique_id:
            raise UnauthorizedException(
                msg.INVALID_TOKEN
            )
        user = (
        db.query(User)
        .filter(User.unique_id == unique_id)
        .first()
        )

        if not user:
            raise UnauthorizedException(
                msg.INVALID_TOKEN
        )
        
        new_access_token = create_access_token(
            unique_id
        )

        return {
            "access_token": new_access_token,
            "token_type":"bearer"
        }