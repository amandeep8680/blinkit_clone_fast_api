from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.userschema import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UpdatedUserResponse,
    UserDeleteResponse,
)
from app.services.user_service import UserService


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
    unique_id: str,
    db: DBSession,
):
    """Get Super Admin details."""

    return user_service.get_admin(
        db=db,
        unique_id=unique_id
    )


@router.patch(
    "/update/{unique_id}",
    response_model=UpdatedUserResponse
)
def update_super_admin(
    unique_id: str,
    user: UserUpdate,
    db: DBSession,
):
    """Update Super Admin."""

    return user_service.update_super_admin(
        db=db,
        unique_id=unique_id,
        user=user
    )


@router.delete(
    "/delete/{unique_id}",
    response_model=UserDeleteResponse
)
def delete_admin(
    unique_id: str,
    db: DBSession,
):
    """Delete Super Admin."""

    return user_service.delete_admin(
        db=db,
        unique_id=unique_id
    )