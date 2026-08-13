from pydantic import BaseModel
from datetime import datetime


class BranchCreate(BaseModel):
    """Schema used to create a new branch."""

    name: str
    address: str
    city: str
    pincode: str


class BranchResponse(BaseModel):
    """Schema returned after creating or fetching a branch."""

    unique_id: str
    name: str
    address: str
    city: str
    pincode: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BranchUpdate(BaseModel):
    """Schema used to update branch information."""

    name: str | None = None
    address: str | None = None
    city: str | None = None
    pincode: str | None = None
    is_active: bool | None = None


class BranchManagerAssign(BaseModel):
    """Schema used to assign or change the manager of a branch."""

    manager_unique_id: str


class BranchDeleteResponse(BaseModel):
    """Schema returned after deleting a branch."""

    unique_id: str
    name: str
    message: str