from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.authorization import require_roles

from app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from app.schemas.product_image_schema import (
    ProductImageCreate,
    ProductImageUpdate,
    ProductImageResponse,
)

from app.services.product_image_service import (
    ProductImageService,
)


product_image_service = ProductImageService()


router = APIRouter(
    prefix="/product-images",
    tags=["Product Images"],
)


# =========================================================
# Add Product Image
# =========================================================
@router.post(
    "",
    response_model=ProductImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_image_route(
    data: ProductImageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_image_service.create_image(
        db,
        data,
    )


# =========================================================
# Get Images By Product
# =========================================================
@router.get(
    "/product/{product_unique_id}",
    response_model=list[ProductImageResponse],
)
def get_product_images_route(
    product_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_image_service.get_images_by_product(
        db,
        product_unique_id,
    )


# =========================================================
# Get Single Product Image
# =========================================================
@router.get(
    "/{image_unique_id}",
    response_model=ProductImageResponse,
)
def get_product_image_route(
    image_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_image_service.get_image(
        db,
        image_unique_id,
    )


# =========================================================
# Update Product Image
# =========================================================
@router.patch(
    "/{image_unique_id}",
    response_model=ProductImageResponse,
)
def update_product_image_route(
    image_unique_id: str,
    data: ProductImageUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_image_service.update_image(
        db,
        image_unique_id,
        data,
    )


# =========================================================
# Delete Product Image
# =========================================================
@router.delete(
    "/{image_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_product_image_route(
    image_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return product_image_service.delete_image(
        db,
        image_unique_id,
    )