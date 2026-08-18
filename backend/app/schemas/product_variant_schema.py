from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProductVariantBase(BaseModel):

    sku: str

    value: str

    unit: str

    mrp: Decimal = Field(
        gt=0,
    )

    selling_price: Decimal = Field(
        gt=0,
    )

    is_active: bool = True


class ProductVariantCreate(
    ProductVariantBase
):
    product_unique_id: str


class ProductVariantUpdate(BaseModel):

    sku: Optional[str] = None

    value: Optional[str] = None

    unit: Optional[str] = None

    mrp: Optional[Decimal] = Field(
        default=None,
        gt=0,
    )

    selling_price: Optional[Decimal] = Field(
        default=None,
        gt=0,
    )

    is_active: Optional[bool] = None


class ProductVariantResponse(
    ProductVariantBase
):
    unique_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )