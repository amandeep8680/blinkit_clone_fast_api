from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from  app.database.database import get_db

from  app.auth.authorization import require_roles

from  app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from  app.schemas.subcategory_schema import (
    SubCategoryCreate,
    SubCategoryUpdate,
    SubCategoryResponse,
)

from  app.services.subcategory_service import (
    SubCategoryService,
)


subcategory_service = SubCategoryService()

DBSession = Annotated[
    Session,
    Depends(get_db),
]

router = APIRouter(
    prefix="/subcategories",
    tags=["SubCategories"],
)


# =========================================================
# Create SubCategory
# =========================================================
# category_unique_id is provided in request body.
#
# Service resolves:
# category_unique_id -> Category.id
#
# Then saves:
# subcategory.category_id = category.id
#
# Success:
# - 201 Created
#
# Possible errors:
# - 404 Category not found
# - 409 SubCategory already exists
@router.post(
    "",
    response_model=SubCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subcategory_route(
    data: SubCategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return subcategory_service.create_subcategory(
        db,
        data,
    )


# =========================================================
# Get All SubCategories
# =========================================================
@router.get(
    "",
    response_model=list[SubCategoryResponse],
)
def get_all_subcategories_route(
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
    return subcategory_service.get_all_subcategories(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Active SubCategories
# =========================================================
@router.get(
    "/active",
    response_model=list[SubCategoryResponse],
)
def get_active_subcategories_route(
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
    return subcategory_service.get_active_subcategories(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get SubCategories By Category
# =========================================================
# Example:
# /subcategories/category/{category_unique_id}
#
# Returns all subcategories belonging
# to the requested category.
@router.get(
    "/category/{category_unique_id}",
    response_model=list[SubCategoryResponse],
)
def get_subcategories_by_category_route(
    category_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return (
        subcategory_service
        .get_subcategories_by_category(
            db,
            category_unique_id,
        )
    )


# =========================================================
# Get Single SubCategory
# =========================================================
@router.get(
    "/{subcategory_unique_id}",
    response_model=SubCategoryResponse,
)
def get_subcategory_route(
    subcategory_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return subcategory_service.get_subcategory(
        db,
        subcategory_unique_id,
    )


# =========================================================
# Update SubCategory
# =========================================================
@router.patch(
    "/{subcategory_unique_id}",
    response_model=SubCategoryResponse,
)
def update_subcategory_route(
    subcategory_unique_id: str,
    data: SubCategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return subcategory_service.update_subcategory(
        db,
        subcategory_unique_id,
        data,
    )


# =========================================================
# Activate SubCategory
# =========================================================
@router.patch(
    "/{subcategory_unique_id}/activate",
    response_model=SubCategoryResponse,
)
def activate_subcategory_route(
    subcategory_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return subcategory_service.activate_subcategory(
        db,
        subcategory_unique_id,
    )


# =========================================================
# Deactivate SubCategory
# =========================================================
@router.patch(
    "/{subcategory_unique_id}/deactivate",
    response_model=SubCategoryResponse,
)
def deactivate_subcategory_route(
    subcategory_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return (
        subcategory_service
        .deactivate_subcategory(
            db,
            subcategory_unique_id,
        )
    )


# =========================================================
# Delete SubCategory
# =========================================================
@router.delete(
    "/{subcategory_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_subcategory_route(
    subcategory_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return subcategory_service.delete_subcategory(
        db,
        subcategory_unique_id,
    )