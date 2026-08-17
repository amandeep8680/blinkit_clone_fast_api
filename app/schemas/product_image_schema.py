from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProductImageBase(BaseModel):

    image_url: str

    sort_order: int = Field(
        default=0,
        ge=0,
    )

    is_primary: bool = False


class ProductImageCreate(
    ProductImageBase
):
    product_unique_id: str


class ProductImageUpdate(BaseModel):

    image_url: Optional[str] = None

    sort_order: Optional[int] = Field(
        default=None,
        ge=0,
    )

    is_primary: Optional[bool] = None


class ProductImageResponse(
    ProductImageBase
):
    unique_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )