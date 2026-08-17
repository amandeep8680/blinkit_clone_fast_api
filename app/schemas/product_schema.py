from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.schemas.product_variant_schema import (
    ProductVariantResponse,
)

from app.schemas.product_image_schema import (
    ProductImageResponse,
)


class ProductBase(BaseModel):

    name: str

    slug: str

    description: Optional[str] = None

    is_active: bool = True


class ProductCreate(
    ProductBase
):
    brand_unique_id: str

    subcategory_unique_id: str


class ProductUpdate(BaseModel):

    name: Optional[str] = None

    slug: Optional[str] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


class ProductResponse(
    ProductBase
):
    unique_id: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductWithDetailsResponse(
    ProductResponse
):
    variants: list[
        ProductVariantResponse
    ] = Field(
        default_factory=list
    )

    images: list[
        ProductImageResponse
    ] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductBrandResponse(BaseModel):

    unique_id: str
    name: str
    slug: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductSubCategoryResponse(BaseModel):

    unique_id: str
    name: str
    slug: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductFullResponse(
    ProductResponse
):
    brand: ProductBrandResponse

    subcategory: ProductSubCategoryResponse

    variants: list[
        ProductVariantResponse
    ] = Field(
        default_factory=list
    )

    images: list[
        ProductImageResponse
    ] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )