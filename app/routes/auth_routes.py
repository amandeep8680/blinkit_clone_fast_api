from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth_schema import (
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()

DBSession = Annotated[
    Session,
    Depends(get_db)
]


@router.post(
    "/login",
    response_model=TokenResponse
    )

def login(
    credentials: LoginRequest,
    db: DBSession,
):
    return auth_service.login(
        db=db,
        credentials=credentials
    )