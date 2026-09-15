from fastapi import APIRouter, Depends, Request

from typing import Annotated
from sqlalchemy.orm import Session
import traceback
from app.database.database import get_db

from app.schemas.auth_schema import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


DBSession = Annotated[
    Session,
    Depends(get_db),
]


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: Request,
    credentials: LoginRequest,
    db: DBSession,
):
    try:
        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        return auth_service.login(
            db=db,
            credentials=credentials,
            client_ip=client_ip,
        )

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        traceback.print_exc()
        raise


# =========================================================
# REFRESH ACCESS TOKEN
# =========================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
def refresh_token(
    db: DBSession,
    data: RefreshTokenRequest,
):
    return auth_service.refresh_access_token(
        db=db,
        refresh_token=data.refresh_token,
    )


# =========================================================
# REQUEST PASSWORD RESET
# =========================================================

@router.post(
    "/password-reset/request",
)
def request_password_reset(
    request: Request,
    data: PasswordResetRequest,
    db: DBSession,
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    return auth_service.request_password_reset(
        db=db,
        email=data.email,
        client_ip=client_ip,
    )


# =========================================================
# CONFIRM PASSWORD RESET
# =========================================================

@router.post(
    "/password-reset/confirm",
)
def confirm_password_reset(
    request: Request,
    data: PasswordResetConfirm,
    db: DBSession,
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    return auth_service.confirm_password_reset(
        db=db,
        email=data.email,
        otp=data.otp,
        new_password=data.new_password,
        client_ip=client_ip,
    )