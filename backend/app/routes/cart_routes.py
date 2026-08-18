from fastapi import (
    APIRouter,
    Depends,
    status,
)

from typing import Annotated
from sqlalchemy.orm import Session

from  app.database.database import get_db

from  app.auth.authorization import require_roles
from  app.constants import roles

from  app.schemas.cart_schema import (
    CartCreate,
    CartResponse,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
)

from  app.services.cart_service import (
    CartService,
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


# Service instance
cart_service = CartService()


# Database dependency
DBSession = Annotated[
    Session,
    Depends(get_db),
]


# Customer authentication dependency
CurrentCustomer = Annotated[
    object,
    Depends(
        require_roles(
            roles.CUSTOMER
        )
    ),
]


# =========================================================
# Create Cart
# =========================================================
@router.post(
    "",
    response_model=CartResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cart(
    data: CartCreate,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.create_cart(
        db=db,
        customer=current_user,
        data=data,
    )


# =========================================================
# Get Current Customer Cart
# =========================================================
@router.get(
    "",
    response_model=CartResponse,
)
def get_cart(
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.get_active_cart(
        db=db,
        customer=current_user,
    )


# =========================================================
# Add Product Variant To Cart
# =========================================================
@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_cart_item(
    data: CartItemCreate,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.add_item(
        db=db,
        customer=current_user,
        data=data,
    )


# =========================================================
# Update Cart Item Quantity
# =========================================================
@router.patch(
    "/items/{product_variant_unique_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    product_variant_unique_id: str,
    data: CartItemUpdate,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.update_item(
        db=db,
        customer=current_user,
        product_variant_unique_id=product_variant_unique_id,
        data=data,
    )


# =========================================================
# Remove Item From Cart
# =========================================================
@router.delete(
    "/items/{product_variant_unique_id}",
    status_code=status.HTTP_200_OK,
)
def remove_cart_item(
    product_variant_unique_id: str,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.remove_item(
        db=db,
        customer=current_user,
        product_variant_unique_id=product_variant_unique_id,
    )


# =========================================================
# Clear Complete Cart items
# =========================================================
@router.delete(
    "/clear",
    status_code=status.HTTP_200_OK,
)
def clear_cart_items(
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.clear_cart(
        db=db,
        customer=current_user,
    )

# =========================================================
# Delete Complete Cart 
# =========================================================
@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
)
def delete_cart(
    db: DBSession,
    current_user: CurrentCustomer,
):
    return cart_service.delete_cart(
        db=db,
        customer=current_user,
    )