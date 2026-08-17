# app/schemas/branch_inventory_schema.py

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BranchInventoryCreate(BaseModel):
    branch_unique_id: str
    product_variant_unique_id: str

    stock_quantity: int = Field(
        default=0,
        ge=0,
    )

    selling_price_override: Optional[Decimal] = Field(
        default=None,
        gt=0,
    )

    is_available: bool = True


class BranchInventoryUpdate(BaseModel):
    stock_quantity: Optional[int] = Field(
        default=None,
        ge=0,
    )

    selling_price_override: Optional[Decimal] = Field(
        default=None,
        gt=0,
    )

    is_available: Optional[bool] = None


class StockUpdate(BaseModel):
    quantity: int = Field(
        gt=0,
    )


class BranchInventoryResponse(BaseModel):
    stock_quantity: int
    selling_price_override: Optional[Decimal] = None
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )