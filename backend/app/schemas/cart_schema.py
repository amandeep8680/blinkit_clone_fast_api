from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# =========================================================
# Cart Create
# =========================================================

class CartCreate(BaseModel):
    branch_unique_id: str


# =========================================================
# Cart Item
# =========================================================

class CartItemCreate(BaseModel):
    product_variant_unique_id: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        gt=0,
    )


# Small ProductVariant response for cart
class CartProductVariantResponse(BaseModel):
    unique_id: str
    sku: str
    value: str
    unit: str
    mrp: Decimal
    selling_price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class CartItemResponse(BaseModel):
    quantity: int

    is_available: bool
    available_stock: int
    availability_message: str | None = None

    product_variant: CartProductVariantResponse

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )



# =========================================================
# Cart Response
# =========================================================

class CartBranchResponse(BaseModel):
    unique_id: str
    name: str
    city: str

    model_config = ConfigDict(
        from_attributes=True
    )

class CartResponse(BaseModel):
    is_active: bool
    can_checkout: bool

    branch: CartBranchResponse

    items: list[CartItemResponse] = Field(
        default_factory=list
    )

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )