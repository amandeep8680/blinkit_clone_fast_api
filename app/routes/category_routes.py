# app/routes/category_routes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.authorization import require_roles
from app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryWithSubCategoriesResponse,
)

from app.services.category_service import CategoryService


# Single service instance
category_service = CategoryService()


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# =========================================================
# Create Category
# =========================================================
# Allowed roles:
# - Super Admin
# - Branch Manager
#
# Success:
# - 201 Created
#
# Possible errors:
# - 409 Conflict -> Category already exists
@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category_route(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.create_category(
        db,
        data,
    )


# =========================================================
# Get All Categories
# =========================================================
# Returns active + inactive categories.
#
# Supports pagination using:
# - skip
# - limit
@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_all_categories_route(
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
    return category_service.get_all_categories(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Active Categories
# =========================================================
# Returns only categories where:
# is_active = True
@router.get(
    "/active",
    response_model=list[CategoryResponse],
)
def get_active_categories_route(
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
    return category_service.get_active_categories(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Category With SubCategories
# =========================================================
# Returns category details with all related subcategories.
#
# SQLAlchemy relationship used:
# category.subcategories
@router.get(
    "/{category_unique_id}/subcategories",
    response_model=CategoryWithSubCategoriesResponse,
)
def get_category_with_subcategories_route(
    category_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.get_category(
        db,
        category_unique_id,
    )


# =========================================================
# Get Single Category
# =========================================================
# Finds category using public unique_id.
#
# Possible errors:
# - 404 Not Found -> Category does not exist
@router.get(
    "/{category_unique_id}",
    response_model=CategoryResponse,
)
def get_category_route(
    category_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.get_category(
        db,
        category_unique_id,
    )


# =========================================================
# Update Category
# =========================================================
# Partial update using PATCH.
#
# Possible errors:
# - 404 Not Found
# - 409 Conflict -> duplicate name or slug
@router.patch(
    "/{category_unique_id}",
    response_model=CategoryResponse,
)
def update_category_route(
    category_unique_id: str,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.update_category(
        db,
        category_unique_id,
        data,
    )


# =========================================================
# Activate Category
# =========================================================
# Changes:
# is_active = True
#
# Possible errors:
# - 404 Not Found
# - 400 Bad Request -> already active
@router.patch(
    "/{category_unique_id}/activate",
    response_model=CategoryResponse,
)
def activate_category_route(
    category_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.activate_category(
        db,
        category_unique_id,
    )


# =========================================================
# Deactivate Category
# =========================================================
# Changes:
# is_active = False
#
# Possible errors:
# - 404 Not Found
# - 400 Bad Request -> already inactive
@router.patch(
    "/{category_unique_id}/deactivate",
    response_model=CategoryResponse,
)
def deactivate_category_route(
    category_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.deactivate_category(
        db,
        category_unique_id,
    )


# =========================================================
# Delete Category
# =========================================================
# Permanently deletes category.
#
# If relationship has:
# cascade="all, delete-orphan"
#
# then its related subcategories can also be deleted.
@router.delete(
    "/{category_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_category_route(
    category_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return category_service.delete_category(
        db,
        category_unique_id,
    )