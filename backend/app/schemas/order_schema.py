from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# =========================================================
# Checkout
# =========================================================

class OrderCreate(BaseModel):
    address_unique_id: str

    payment_method: str = "cod"

    customer_note: Optional[str] = None


# =========================================================
# Order Item Response
# =========================================================

class OrderItemResponse(BaseModel):
    product_name: str

    variant_value: str
    variant_unit: str
    sku: str

    quantity: int

    mrp: Decimal
    unit_price: Decimal
    total_price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Order History
# =========================================================

class OrderHistoryResponse(BaseModel):
    status: str
    note: Optional[str] = None

    changed_by_unique_id: str
    changed_by_role: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Change Order Status
# =========================================================

class OrderStatusUpdate(BaseModel):
    status: str
    note: Optional[str] = None


# =========================================================
# Payment Status Update
# =========================================================

class PaymentStatusUpdate(BaseModel):
    payment_status: str


# =========================================================
# Order Response
# =========================================================

class OrderResponse(BaseModel):
    unique_id: str

    status: str

    payment_method: str
    payment_status: str

    subtotal: Decimal
    delivery_charge: Decimal
    discount_amount: Decimal
    total_amount: Decimal

    customer_note: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Detailed Order
# =========================================================

class OrderDetailResponse(OrderResponse):
    address_label: str
    address_line: str
    landmark: Optional[str] = None
    city: str
    state: str
    pincode: str

    items: list[OrderItemResponse] = Field(
        default_factory=list
    )

    history: list[OrderHistoryResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )