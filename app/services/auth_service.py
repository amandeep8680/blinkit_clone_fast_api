from sqlalchemy.orm import Session

from app.models.admin_model import User
from app.models.branchmanager_model import BranchManager

from app.schemas.auth_schema import LoginRequest

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

from app.exceptions.custom_exceptions import (
    UnauthorizedException,
)

from app.exceptions import messages as msg


class AuthService:

    def login(
        self,
        db: Session,
        credentials: LoginRequest,
    ):
        """
        Authenticate an Admin or Branch Manager
        and return access and refresh tokens.
        """

        # First, try to find the user in the Admin table.
        current_user = (
            db.query(User)
            .filter(User.email == credentials.email)
            .first()
        )

        # If no Admin exists with this email,
        # try to find a Branch Manager.
        if not current_user:
            current_user = (
                db.query(BranchManager)
                .filter(
                    BranchManager.email
                    == credentials.email
                )
                .first()
            )

        # No user exists with the provided email.
        if not current_user:
            raise UnauthorizedException(
                msg.INVALID_CREDENTIALS
            )

        # Verify the provided password against
        # the stored hashed password.
        if not verify_password(
            credentials.password,
            current_user.password_hash,
        ):
            raise UnauthorizedException(
                msg.INVALID_CREDENTIALS
            )

        # Prevent inactive users from logging in.
        if not current_user.is_active:
            raise UnauthorizedException(
                msg.USER_INACTIVE
            )

        # Generate JWT tokens using the role
        # stored on the authenticated user.
        access_token = create_access_token(
            unique_id=current_user.unique_id,
            role=current_user.role,
        )

        refresh_token = create_refresh_token(
            unique_id=current_user.unique_id,
            role=current_user.role,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


    def refresh_access_token(
        self,
        db: Session,
        refresh_token: str,
        ):
        """
        Generate a new access token using a valid refresh token.
        """

        # 1. Refresh token ko decode karo
        payload = decode_token(refresh_token)

        # 2. Check karo ki token actually refresh token hai
        if payload.get("type") != "refresh":
            raise UnauthorizedException(
                msg.INVALID_TOKEN
            )

        # 3. Token se user information nikalo
        unique_id = payload.get("sub")
        role = payload.get("role")

        if not unique_id or not role:
            raise UnauthorizedException(
                msg.INVALID_TOKEN
            )

        # 4. User Admin table me search karo
        current_user = (
            db.query(User)
            .filter(User.unique_id == unique_id)
            .first()
        )

        # 5. Admin nahi mila to BranchManager me search karo
        if not current_user:
            current_user = (
                db.query(BranchManager)
                .filter(
                    BranchManager.unique_id == unique_id
                )
                .first()
            )

        # 6. User exist nahi karta
        if not current_user:
            raise UnauthorizedException(
                msg.INVALID_TOKEN
            )

        # 7. Inactive user ko new token mat do
        if not current_user.is_active:
            raise UnauthorizedException(
                msg.USER_INACTIVE
            )

        # 8. Naya access token banao
        access_token = create_access_token(
            unique_id=current_user.unique_id,
            role=current_user.role,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }