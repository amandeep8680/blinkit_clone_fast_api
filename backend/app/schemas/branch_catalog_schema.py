from decimal import Decimal
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# =========================================================
# Product Image
# =========================================================

class CatalogImageResponse(BaseModel):
    image_url: str
    sort_order: int
    is_primary: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Brand
# =========================================================

class CatalogBrandResponse(BaseModel):
    unique_id: str
    name: str
    slug: str
    logo_url: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# SubCategory
# =========================================================

class CatalogSubCategoryResponse(BaseModel):
    unique_id: str
    name: str
    slug: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Variant
# =========================================================

class CatalogVariantResponse(BaseModel):
    unique_id: str
    sku: str
    value: str
    unit: str

    mrp: Decimal
    selling_price: Decimal

    is_available: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# Product
# =========================================================

class BranchCatalogProductResponse(BaseModel):
    unique_id: str
    name: str
    slug: str
    description: Optional[str] = None

    brand: CatalogBrandResponse
    subcategory: CatalogSubCategoryResponse

    images: list[CatalogImageResponse] = Field(
        default_factory=list
    )

    variants: list[CatalogVariantResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )