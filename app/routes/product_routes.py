from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.authorization import require_roles

from app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductFullResponse,
)

from app.services.product_service import ProductService


product_service = ProductService()


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# =========================================================
# Create Product
# =========================================================
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_route(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.create_product(
        db,
        data,
    )


# =========================================================
# Get All Products
# =========================================================
@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_all_products_route(
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
    return product_service.get_all_products(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Active Products
# =========================================================
@router.get(
    "/active",
    response_model=list[ProductResponse],
)
def get_active_products_route(
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
    return product_service.get_active_products(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Product With Details
# =========================================================
# Returns:
# - Product
# - Brand
# - SubCategory
# - Variants
# - Images
@router.get(
    "/{product_unique_id}/details",
    response_model=ProductFullResponse,
)
def get_product_details_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.get_product(
        db,
        product_unique_id,
    )


# =========================================================
# Get Single Product
# =========================================================
@router.get(
    "/{product_unique_id}",
    response_model=ProductResponse,
)
def get_product_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.get_product(
        db,
        product_unique_id,
    )


# =========================================================
# Update Product
# =========================================================
@router.patch(
    "/{product_unique_id}",
    response_model=ProductResponse,
)
def update_product_route(
    product_unique_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.update_product(
        db,
        product_unique_id,
        data,
    )


# =========================================================
# Activate Product
# =========================================================
@router.patch(
    "/{product_unique_id}/activate",
    response_model=ProductResponse,
)
def activate_product_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.activate_product(
        db,
        product_unique_id,
    )


# =========================================================
# Deactivate Product
# =========================================================
@router.patch(
    "/{product_unique_id}/deactivate",
    response_model=ProductResponse,
)
def deactivate_product_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.deactivate_product(
        db,
        product_unique_id,
    )


# =========================================================
# Delete Product
# =========================================================
@router.delete(
    "/{product_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_product_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_service.delete_product(
        db,
        product_unique_id,
    )