import hashlib
import os
import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admin_model import User
from app.models.branchmanager_model import BranchManager
from app.models.customer_model import Customer

from app.schemas.auth_schema import LoginRequest

from app.core.redis import redis_client

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

from app.core.login_protection import (
    MAX_FAILED_ATTEMPTS,
    is_login_blocked,
    record_failed_login,
    reset_failed_logins,
)

from app.exceptions.custom_exceptions import (
    UnauthorizedException,
)

from app.exceptions import messages as msg


# =========================================================
# CONFIG
# =========================================================

LOGIN_RATE_LIMIT = int(
    os.getenv(
        "LOGIN_RATE_LIMIT",
        "10",
    )
)

LOGIN_RATE_WINDOW = int(
    os.getenv(
        "LOGIN_RATE_WINDOW",
        "60",
    )
)


PASSWORD_RESET_MAX_REQUESTS = int(
    os.getenv(
        "PASSWORD_RESET_MAX_REQUESTS",
        "3",
    )
)

PASSWORD_RESET_RATE_WINDOW = int(
    os.getenv(
        "PASSWORD_RESET_RATE_WINDOW",
        "900",
    )
)

PASSWORD_RESET_OTP_TTL = int(
    os.getenv(
        "PASSWORD_RESET_OTP_TTL",
        "600",
    )
)

PASSWORD_RESET_MAX_OTP_ATTEMPTS = int(
    os.getenv(
        "PASSWORD_RESET_MAX_OTP_ATTEMPTS",
        "5",
    )
)


class AuthService:

    # =====================================================
    # COMMON USER FINDER
    # =====================================================

    def _find_user_by_email(
        self,
        db: Session,
        email: str,
    ):
        email = email.strip().lower()

        # -----------------------------
        # Super Admin
        # -----------------------------
        current_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if current_user:
            return current_user

        # -----------------------------
        # Branch Manager
        # -----------------------------
        current_user = (
            db.query(BranchManager)
            .filter(
                BranchManager.email == email
            )
            .first()
        )

        if current_user:
            return current_user

        # -----------------------------
        # Customer
        # -----------------------------
        return (
            db.query(Customer)
            .filter(
                Customer.email == email
            )
            .first()
        )

    # =====================================================
    # LOGIN RATE LIMIT
    # =====================================================

    def _login_rate_key(
        self,
        ip: str,
        email: str,
    ):
        return (
            f"auth:login:rate:"
            f"{ip}:{email.lower()}"
        )

    def _check_login_rate_limit(
        self,
        ip: str,
        email: str,
    ):
        key = self._login_rate_key(
            ip=ip,
            email=email,
        )

        attempts = redis_client.incr(key)

        # First request par TTL lagao
        if attempts == 1:
            redis_client.expire(
                key,
                LOGIN_RATE_WINDOW,
            )

        if attempts > LOGIN_RATE_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Too many login requests. "
                    "Try again later."
                ),
            )

    # =====================================================
    # LOGIN
    # =====================================================

    def login(
        self,
        db: Session,
        credentials: LoginRequest,
        client_ip: str,
    ):
        """
        Authenticate Super Admin,
        Branch Manager or Customer.
        """

        email = credentials.email.strip().lower()

        # -----------------------------------
        # 1. General login rate limit
        # -----------------------------------
        self._check_login_rate_limit(
            ip=client_ip,
            email=email,
        )

        # -----------------------------------
        # 2. Failed login brute-force block
        # -----------------------------------
        if is_login_blocked(
            ip=client_ip,
            email=email,
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "Too many failed login attempts. "
                    "Try again later."
                ),
            )

        # -----------------------------------
        # 3. Find user
        # -----------------------------------
        current_user = self._find_user_by_email(
            db=db,
            email=email,
        )

        # -----------------------------------
        # 4. User not found
        # -----------------------------------
        if not current_user:

            attempts = record_failed_login(
                ip=client_ip,
                email=email,
            )

            if attempts >= MAX_FAILED_ATTEMPTS:
                raise HTTPException(
                    status_code=429,
                    detail=(
                        "Too many failed login attempts. "
                        "Try again later."
                    ),
                )

            raise UnauthorizedException(
                msg.INVALID_CREDENTIALS
            )

        # -----------------------------------
        # 5. Verify password
        # -----------------------------------
        if not verify_password(
            credentials.password,
            current_user.password_hash,
        ):

            attempts = record_failed_login(
                ip=client_ip,
                email=email,
            )

            if attempts >= MAX_FAILED_ATTEMPTS:
                raise HTTPException(
                    status_code=429,
                    detail=(
                        "Too many failed login attempts. "
                        "Try again later."
                    ),
                )

            raise UnauthorizedException(
                msg.INVALID_CREDENTIALS
            )

        # -----------------------------------
        # 6. Block inactive account
        # -----------------------------------
        if not current_user.is_active:
            raise UnauthorizedException(
                msg.USER_INACTIVE
            )

        # -----------------------------------
        # 7. Successful login
        # Reset failed login counter
        # -----------------------------------
        reset_failed_logins(
            ip=client_ip,
            email=email,
        )

        # -----------------------------------
        # 8. Access Token
        # -----------------------------------
        access_token = create_access_token(
            unique_id=current_user.unique_id,
            role=current_user.role,
        )

        # -----------------------------------
        # 9. Refresh Token
        # -----------------------------------
        refresh_token = create_refresh_token(
            unique_id=current_user.unique_id,
            role=current_user.role,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # =====================================================
    # REFRESH ACCESS TOKEN
    # =====================================================

    def refresh_access_token(
        self,
        db: Session,
        refresh_token: str,
    ):
        # -----------------------------------
        # Decode refresh token
        # -----------------------------------
        payload = decode_token(
            refresh_token
        )

        # -----------------------------------
        # Must be refresh token
        # -----------------------------------
        if payload.get("type") != "refresh":
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
        # Search Super Admin
        # -----------------------------------
        current_user = (
            db.query(User)
            .filter(
                User.unique_id == unique_id
            )
            .first()
        )

        # -----------------------------------
        # Search Branch Manager
        # -----------------------------------
        if not current_user:
            current_user = (
                db.query(BranchManager)
                .filter(
                    BranchManager.unique_id
                    == unique_id
                )
                .first()
            )

        # -----------------------------------
        # Search Customer
        # -----------------------------------
        if not current_user:
            current_user = (
                db.query(Customer)
                .filter(
                    Customer.unique_id
                    == unique_id
                )
                .first()
            )

        if not current_user:
            raise UnauthorizedException(
                msg.INVALID_TOKEN
            )

        if not current_user.is_active:
            raise UnauthorizedException(
                msg.USER_INACTIVE
            )

        # -----------------------------------
        # Generate new access token
        # -----------------------------------
        access_token = create_access_token(
            unique_id=current_user.unique_id,
            role=current_user.role,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    # =====================================================
    # PASSWORD RESET KEYS
    # =====================================================

    def _password_reset_rate_key(
        self,
        ip: str,
        email: str,
    ):
        return (
            f"auth:password_reset:rate:"
            f"{ip}:{email.lower()}"
        )

    def _password_reset_otp_key(
        self,
        email: str,
    ):
        return (
            f"auth:password_reset:otp:"
            f"{email.lower()}"
        )

    def _password_reset_attempt_key(
        self,
        ip: str,
        email: str,
    ):
        return (
            f"auth:password_reset:attempt:"
            f"{ip}:{email.lower()}"
        )

    # =====================================================
    # REQUEST PASSWORD RESET
    # =====================================================

    def request_password_reset(
        self,
        db: Session,
        email: str,
        client_ip: str,
    ):
        email = email.strip().lower()

        # -----------------------------------
        # 1. Rate limit
        # -----------------------------------
        rate_key = (
            self._password_reset_rate_key(
                ip=client_ip,
                email=email,
            )
        )

        requests = redis_client.incr(
            rate_key
        )

        if requests == 1:
            redis_client.expire(
                rate_key,
                PASSWORD_RESET_RATE_WINDOW,
            )

        if (
            requests
            > PASSWORD_RESET_MAX_REQUESTS
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "Too many password reset "
                    "requests. Try again later."
                ),
            )

        # -----------------------------------
        # 2. Find account
        # -----------------------------------
        current_user = (
            self._find_user_by_email(
                db=db,
                email=email,
            )
        )

        # -----------------------------------
        # Don't reveal whether email exists
        # -----------------------------------
        if not current_user:
            return {
                "message": (
                    "If an account exists with "
                    "this email, a password reset "
                    "code has been sent."
                )
            }

        # -----------------------------------
        # 3. Generate OTP
        # -----------------------------------
        # otp = (
        #     f"{secrets.randbelow(1_000_000):06d}"
        # )


        # TODO: TESTING ONLY - replace with random OTP before production
        otp = "123456"
        # -----------------------------------
        # 4. Hash OTP
        # -----------------------------------
        otp_hash = hashlib.sha256(
            otp.encode()
        ).hexdigest()

        otp_key = (
            self._password_reset_otp_key(
                email=email
            )
        )

        # -----------------------------------
        # 5. Store OTP in Redis
        # -----------------------------------
        redis_client.set(
            otp_key,
            otp_hash,
            ex=PASSWORD_RESET_OTP_TTL,
        )

        # -----------------------------------
        # Reset old OTP failed attempts
        # -----------------------------------
        attempt_key = (
            self._password_reset_attempt_key(
                ip=client_ip,
                email=email,
            )
        )

        redis_client.delete(
            attempt_key
        )

        # ===================================
        # SEND EMAIL HERE
        # ===================================

        # Example:
        #
        # send_password_reset_otp(
        #     email=email,
        #     otp=otp,
        # )

        # DEV ONLY:
        print(
            f"PASSWORD RESET OTP = {otp}"
        )

        return {
            "message": (
                "If an account exists with "
                "this email, a password reset "
                "code has been sent."
            )
        }

    # =====================================================
    # CONFIRM PASSWORD RESET
    # =====================================================

    def confirm_password_reset(
        self,
        db: Session,
        email: str,
        otp: str,
        new_password: str,
        client_ip: str,
    ):
        email = email.strip().lower()

        otp_key = (
            self._password_reset_otp_key(
                email=email
            )
        )

        attempt_key = (
            self._password_reset_attempt_key(
                ip=client_ip,
                email=email,
            )
        )

        # -----------------------------------
        # 1. Check OTP brute-force limit
        # -----------------------------------
        attempts = redis_client.get(
            attempt_key
        )

        if (
            attempts is not None
            and int(attempts)
            >= PASSWORD_RESET_MAX_OTP_ATTEMPTS
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "Too many invalid reset attempts. "
                    "Try again later."
                ),
            )

        # -----------------------------------
        # 2. Get OTP hash
        # -----------------------------------
        stored_otp_hash = (
            redis_client.get(
                otp_key
            )
        )

        if stored_otp_hash is None:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired reset code."
                ),
            )

        # -----------------------------------
        # 3. Hash received OTP
        # -----------------------------------
        received_otp_hash = (
            hashlib.sha256(
                otp.encode()
            ).hexdigest()
        )

        # -----------------------------------
        # 4. Wrong OTP
        # -----------------------------------
        if (
            received_otp_hash
            != stored_otp_hash
        ):
            failed_attempts = (
                redis_client.incr(
                    attempt_key
                )
            )

            if failed_attempts == 1:
                redis_client.expire(
                    attempt_key,
                    PASSWORD_RESET_OTP_TTL,
                )

            # Too many wrong OTPs
            if (
                failed_attempts
                >= PASSWORD_RESET_MAX_OTP_ATTEMPTS
            ):
                # Invalidate OTP
                redis_client.delete(
                    otp_key
                )

                raise HTTPException(
                    status_code=429,
                    detail=(
                        "Too many invalid "
                        "reset attempts."
                    ),
                )

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired reset code."
                ),
            )

        # -----------------------------------
        # 5. Find user
        # -----------------------------------
        current_user = (
            self._find_user_by_email(
                db=db,
                email=email,
            )
        )

        if not current_user:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired reset code."
                ),
            )

        # -----------------------------------
        # 6. Hash new password
        # -----------------------------------
        current_user.password_hash = (
            hash_password(
                new_password
            )
        )

        # -----------------------------------
        # 7. Update DB
        # -----------------------------------
        db.commit()

        # -----------------------------------
        # 8. Delete used OTP + attempts
        # -----------------------------------
        redis_client.delete(
            otp_key,
            attempt_key,
        )

        return {
            "message": (
                "Password reset successfully."
            )
        }