# app/schemas/customer_schema.py

from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# =========================================================
# Customer Schemas
# =========================================================

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class CustomerCreate(CustomerBase):
    password: str = Field(min_length=6)


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):
    unique_id: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Customer Address Schemas
# =========================================================

class CustomerAddressBase(BaseModel):
    label: str
    address_line: str
    landmark: Optional[str] = None
    city: str
    state: str
    pincode: str
    is_default: bool = False


class CustomerAddressCreate(CustomerAddressBase):
    pass


class CustomerAddressUpdate(BaseModel):
    label: Optional[str] = None
    address_line: Optional[str] = None
    landmark: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    is_default: Optional[bool] = None


class CustomerAddressResponse(CustomerAddressBase):
    unique_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Customer With Addresses
# =========================================================

class CustomerWithAddressesResponse(CustomerResponse):
    addresses: list[CustomerAddressResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )