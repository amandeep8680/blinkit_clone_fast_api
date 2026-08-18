# app/routes/brand_routes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from  app.database.database import get_db
from  app.auth.authorization import require_roles
from  app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from  app.schemas.brand_schema import (
    BrandCreate,
    BrandUpdate,
    BrandResponse,
)

from  app.services.brand_service import BrandService


# Create a single service instance.
# All brand routes will use this object
# to call the business logic layer.
brand_service = BrandService()


router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
)


# =========================================================
# Create Brand
# =========================================================
# Allowed roles:
# - Super Admin
# - Branch Manager
#
# Success:
# - 201 Created
#
# Possible exceptions are handled inside the service:
# - 409 Conflict -> Brand already exists
# - 401 Unauthorized -> Invalid/missing authentication
# - 403 Forbidden -> Role not allowed
@router.post(
    "",
    response_model=BrandResponse,
)
def create_brand_route(
    data: BrandCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return brand_service.create_brand(
        db,
        data,
    )


# =========================================================
# Get All Brands
# =========================================================
# Returns both active and inactive brands.
#
# Query params:
# - skip  -> pagination offset
# - limit -> maximum number of records
#
# Success:
# - 200 OK
@router.get(
    "",
    response_model=list[BrandResponse],
)
def get_all_brands_route(
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
    return brand_service.get_all_brands(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Active Brands
# =========================================================
# Returns only brands where:
# is_active = True
#
# Success:
# - 200 OK
@router.get(
    "/active",
    response_model=list[BrandResponse],
)
def get_active_brands_route(
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
    return brand_service.get_active_brands(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get Single Brand
# =========================================================
# Finds a brand using its public unique_id,
# not the internal database primary key.
#
# Success:
# - 200 OK
#
# Possible service exception:
# - 404 Not Found
@router.get(
    "/{brand_unique_id}",
    response_model=BrandResponse,
)
def get_brand_route(
    brand_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return brand_service.get_brand(
        db,
        brand_unique_id,
    )


# =========================================================
# Update Brand
# =========================================================
# Supports partial updates using PATCH.
#
# Only fields provided in BrandUpdate
# will be updated.
#
# Success:
# - 200 OK
#
# Possible service exceptions:
# - 404 Not Found
# - 409 Conflict
@router.patch(
    "/{brand_unique_id}",
    response_model=BrandResponse,
)
def update_brand_route(
    brand_unique_id: str,
    data: BrandUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return brand_service.update_brand(
        db,
        brand_unique_id,
        data,
    )


# =========================================================
# Activate Brand
# =========================================================
# Changes:
# is_active = True
#
# Success:
# - 200 OK
#
# Possible service exceptions:
# - 404 Not Found
# - 400 Bad Request -> Brand is already active
@router.patch(
    "/{brand_unique_id}/activate",
    response_model=BrandResponse,
)
def activate_brand_route(
    brand_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return brand_service.activate_brand(
        db,
        brand_unique_id,
    )


# =========================================================
# Deactivate Brand
# =========================================================
# Changes:
# is_active = False
#
# Success:
# - 200 OK
#
# Possible service exceptions:
# - 404 Not Found
# - 400 Bad Request -> Brand is already inactive
@router.patch(
    "/{brand_unique_id}/deactivate",
    response_model=BrandResponse,
)
def deactivate_brand_route(
    brand_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return brand_service.deactivate_brand(
        db,
        brand_unique_id,
    )


# =========================================================
# Delete Brand
# =========================================================
# Permanently deletes the brand from the database.
#
# Success:
# - 200 OK
#
# Possible service exception:
# - 404 Not Found
@router.delete(
    "/{brand_unique_id}",
)
def delete_brand_route(
    brand_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            SUPER_ADMIN,
            BRANCH_MANAGER,
        )
    ),
):
    return brand_service.delete_brand(
        db,
        brand_unique_id,
    )