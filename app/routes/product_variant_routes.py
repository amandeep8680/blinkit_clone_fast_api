from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.authorization import require_roles

from app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from app.schemas.product_variant_schema import (
    ProductVariantCreate,
    ProductVariantUpdate,
    ProductVariantResponse,
)

from app.services.product_variant_service import (
    ProductVariantService,
)


variant_service = ProductVariantService()


router = APIRouter(
    prefix="/product-variants",
    tags=["Product Variants"],
)


# =========================================================
# Create Product Variant
# =========================================================
@router.post(
    "",
    response_model=ProductVariantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_variant_route(
    data: ProductVariantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.create_variant(
        db,
        data,
    )


# =========================================================
# Get All Product Variants
# =========================================================
@router.get(
    "",
    response_model=list[ProductVariantResponse],
)
def get_all_variants_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.get_all_variants(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Variants By Product
# =========================================================
@router.get(
    "/product/{product_unique_id}",
    response_model=list[ProductVariantResponse],
)
def get_variants_by_product_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.get_variants_by_product(
        db,
        product_unique_id,
    )


# =========================================================
# Get Single Product Variant
# =========================================================
@router.get(
    "/{variant_unique_id}",
    response_model=ProductVariantResponse,
)
def get_variant_route(
    variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.get_variant(
        db,
        variant_unique_id,
    )


# =========================================================
# Update Product Variant
# =========================================================
@router.patch(
    "/{variant_unique_id}",
    response_model=ProductVariantResponse,
)
def update_variant_route(
    variant_unique_id: str,
    data: ProductVariantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.update_variant(
        db,
        variant_unique_id,
        data,
    )


# =========================================================
# Activate Product Variant
# =========================================================
@router.patch(
    "/{variant_unique_id}/activate",
    response_model=ProductVariantResponse,
)
def activate_variant_route(
    variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.activate_variant(
        db,
        variant_unique_id,
    )


# =========================================================
# Deactivate Product Variant
# =========================================================
@router.patch(
    "/{variant_unique_id}/deactivate",
    response_model=ProductVariantResponse,
)
def deactivate_variant_route(
    variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.deactivate_variant(
        db,
        variant_unique_id,
    )


# =========================================================
# Delete Product Variant
# =========================================================
@router.delete(
    "/{variant_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_variant_route(
    variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return variant_service.delete_variant(
        db,
        variant_unique_id,
    )