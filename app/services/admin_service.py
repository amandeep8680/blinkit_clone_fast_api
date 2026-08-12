from sqlalchemy.orm import Session

from app.models.admin import User
from app.schemas.admin_schema import UserCreate, UserUpdate
from app.core.security import hash_password

from app.exceptions.custom_exceptions import (
    ConflictException,
    NotFoundException,
)

from app.exceptions import messages as msg


class UserService:

    def create_super_admin(
        self,
        db: Session,
        user: UserCreate
    ):
        """
        Create Admin.

        Only one Super Admin is allowed.
        """

        existing_admin = db.query(User).first()

        if existing_admin:
            raise ConflictException(
                msg.ADMIN_ALREADY_EXISTS
            )

        new_admin = User(
            name=user.name,
            email=user.email,
            password_hash=hash_password(user.password),
            role = "super-admin"
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return new_admin


    def get_admin(
        self,
        db: Session,
        unique_id: str
    ):
        """Get Super Admin using public unique_id."""

        existing_user = (
            db.query(User)
            .filter(User.unique_id == unique_id)
            .first()
        )

        if not existing_user:
            raise NotFoundException(
                msg.USER_NOT_FOUND
            )

        return existing_user


    def update_super_admin(
        self,
        db: Session,
        unique_id: str,
        user: UserUpdate
    ):
        """Update Super Admin."""

        existing_admin = (
            db.query(User)
            .filter(User.unique_id == unique_id)
            .first()
        )

        if not existing_admin:
            raise NotFoundException(
                msg.USER_NOT_FOUND
            )

        existing_admin.name = user.name

        db.commit()
        db.refresh(existing_admin)

        return existing_admin


    def delete_admin(
        self,
        db: Session,
        unique_id: str
    ):
        """Delete Super Admin."""

        existing_user = (
            db.query(User)
            .filter(User.unique_id == unique_id)
            .first()
        )

        if not existing_user:
            raise NotFoundException(
                msg.USER_NOT_FOUND
            )

        response = {
            "message": "User deleted successfully",
            "unique_id": existing_user.unique_id,
            "name": existing_user.name,
        }

        db.delete(existing_user)
        db.commit()
        return response