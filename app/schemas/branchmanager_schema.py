from pydantic import BaseModel, EmailStr
from datetime import datetime


class ManagerBranchResponse(BaseModel):
    """Branch information assigned to the Branch Manager."""

    unique_id: str
    name: str
    address: str
    city: str
    pincode: str
    is_active: bool

    class Config:
        from_attributes = True


class BranchManagerCreate(BaseModel):
    """Schema used to create a new Branch Manager."""

    name: str
    email: EmailStr
    password: str


class BranchManagerResponse(BaseModel):
    """Schema returned after creating or fetching a Branch Manager."""

    unique_id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    # Branch can be None until the manager is assigned to a branch.
    branch: ManagerBranchResponse | None = None

    class Config:
        from_attributes = True


class BranchManagerUpdate(BaseModel):
    """Schema used to update Branch Manager information."""

    name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class BranchManagerDeleteResponse(BaseModel):
    """Schema returned after deleting a Branch Manager."""

    unique_id: str
    name: str
    message: str