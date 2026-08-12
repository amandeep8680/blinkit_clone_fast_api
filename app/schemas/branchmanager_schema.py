from pydantic import BaseModel, EmailStr
from datetime import datetime


class BranchManagerCreate(BaseModel):
    """Schema used to create a new branch manager."""

    name: str
    email: EmailStr
    password: str
    branch_unique_id: str


class BranchManagerResponse(BaseModel):
    """Schema returned after creating or fetching a branch manager."""

    unique_id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BranchManagerUpdate(BaseModel):
    """Schema used to update branch manager information."""

    name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class BranchManagerDeleteResponse(BaseModel):
    """Schema returned after deleting a branch manager."""

    unique_id: str
    name: str
    message: str