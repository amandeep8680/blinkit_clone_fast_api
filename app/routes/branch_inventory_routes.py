from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.authorization import require_roles

from app.constants.roles import (
    SUPER_ADMIN,
    BRANCH_MANAGER,
)

from app.schemas.branch_inventory_schema import (
    BranchInventoryCreate,
    BranchInventoryUpdate,
    BranchInventoryResponse,
    StockUpdate,
)

from app.services.branch_inventory_service import BranchInventoryService


inventory_service = BranchInventoryService()


router = APIRouter(
    prefix="/inventory",
    tags=["Branch Inventory"],
)


# =========================================================
# Create Inventory
# =========================================================
# Creates one inventory entry for:
# Branch + ProductVariant
@router.post(
    "",
    response_model=BranchInventoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory_route(
    data: BranchInventoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.create_inventory(db, data)


# =========================================================
# Get All Inventory
# =========================================================
@router.get(
    "",
    response_model=list[BranchInventoryResponse],
)
def get_all_inventory_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.get_all_inventory(db, skip, limit)


# # =========================================================
# # Get Inventory By Branch
# # =========================================================
# # Returns all inventory items for a branch.
# @router.get(
#     "/branch/{branch_unique_id}",
#     response_model=list[BranchInventoryResponse],
# )
# def get_inventory_by_branch_route(
#     branch_unique_id: str,
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
# ):
#     return inventory_service.get_inventory_by_branch(
#         db,
#         branch_unique_id,
#         skip,
#         limit,
#     )


# =========================================================
# Get Single Inventory Item
# =========================================================
# Inventory is uniquely identified by:
# branch_unique_id + product_variant_unique_id
@router.get(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}",
    response_model=BranchInventoryResponse,
)
def get_inventory_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.get_inventory(
        db,
        branch_unique_id,
        product_variant_unique_id,
    )


# =========================================================
# Update Inventory
# =========================================================
@router.patch(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}",
    response_model=BranchInventoryResponse,
)
def update_inventory_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    data: BranchInventoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.update_inventory(
        db,
        branch_unique_id,
        product_variant_unique_id,
        data,
    )


# =========================================================
# Increase Stock
# =========================================================
@router.patch(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}/increase-stock",
    response_model=BranchInventoryResponse,
)
def increase_stock_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    data: StockUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.increase_stock(
        db,
        branch_unique_id,
        product_variant_unique_id,
        data.quantity,
    )


# =========================================================
# Decrease Stock
# =========================================================
@router.patch(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}/decrease-stock",
    response_model=BranchInventoryResponse,
)
def decrease_stock_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    data: StockUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.decrease_stock(
        db,
        branch_unique_id,
        product_variant_unique_id,
        data.quantity,
    )


# =========================================================
# Activate Inventory
# =========================================================
@router.patch(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}/activate",
    response_model=BranchInventoryResponse,
)
def activate_inventory_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.activate_inventory(
        db,
        branch_unique_id,
        product_variant_unique_id,
    )


# =========================================================
# Deactivate Inventory
# =========================================================
@router.patch(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}/deactivate",
    response_model=BranchInventoryResponse,
)
def deactivate_inventory_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.deactivate_inventory(
        db,
        branch_unique_id,
        product_variant_unique_id,
    )


# =========================================================
# Delete Inventory
# =========================================================
@router.delete(
    "/branch/{branch_unique_id}/variant/{product_variant_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_inventory_route(
    branch_unique_id: str,
    product_variant_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(SUPER_ADMIN, BRANCH_MANAGER)),
):
    return inventory_service.delete_inventory(
        db,
        branch_unique_id,
        product_variant_unique_id,
    )