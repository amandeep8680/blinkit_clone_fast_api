from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.admin_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UpdatedUserResponse,
    UserDeleteResponse,
)
from app.services.admin_service import UserService
from app.auth.dependencies import get_current_user
from app.models.admin_model import User
from app.constants import roles
from app.auth.authorization import require_roles



router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# Service instance
user_service = UserService()


# Database dependency
DBSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/create",
    response_model=UserResponse
)
def create_super_admin(
    user: UserCreate,
    db: DBSession,
):
    """Create Super Admin."""

    return user_service.create_super_admin(
        db=db,
        user=user
    )


@router.get(
    "/get",
    response_model=UserResponse
)
def get_admin(
    db: DBSession,
    current_user: User = Depends(require_roles(roles.SUPER_ADMIN)), 
):
    """Get Super Admin details."""

    return user_service.get_admin(
        db=db,
        unique_id=current_user.unique_id
    )


@router.patch(
    "/update",
    response_model=UpdatedUserResponse
)
def update_super_admin(
    user: UserUpdate,
    db: DBSession,
    current_user: User = Depends(require_roles(roles.SUPER_ADMIN)),
):
    """Update Super Admin."""

    return user_service.update_super_admin(
        db=db,
        unique_id=current_user.unique_id,
        user=user
    )


@router.delete(
    "/delete",
    response_model=UserDeleteResponse
)
def delete_admin(
    db: DBSession,
    current_user: User = Depends(require_roles(roles.SUPER_ADMIN)),
):
    """Delete Super Admin."""

    return user_service.delete_admin(
        db=db,
        unique_id=current_user.unique_id
    )