from fastapi import (
    APIRouter,
    Depends,
)

from typing import Annotated
from sqlalchemy.orm import Session

from  app.database.database import get_db

from  app.auth.authorization import require_roles
from  app.constants import roles

from  app.schemas.branch_catalog_schema import (
    BranchCatalogProductResponse,
)
from  app.constants.roles import CUSTOMER , SUPER_ADMIN , BRANCH_MANAGER

from  app.services.branch_catalog_service import (
    BranchCatalogService,
)


router = APIRouter(
    prefix="/branch-catalog",
    tags=["Branch Catalog"],
)


# Service instance
branch_catalog_service = (
    BranchCatalogService()
)


# Database dependency
DBSession = Annotated[
    Session,
    Depends(get_db),
]


# Customer dependency
CurrentCustomer = Annotated[
    object,
    Depends(
        require_roles(
            roles.CUSTOMER,
            roles.SUPER_ADMIN,
            roles.BRANCH_MANAGER
        )
    ),
]


# =========================================================
# Get Selected Branch Catalog
# =========================================================
#
# Customer selects a branch.
#
# Returns only:
# - active Products
# - active ProductVariants
# - available BranchInventory
# - stock > 0
#
@router.get(
    "/{branch_unique_id}",
    response_model=list[
        BranchCatalogProductResponse
    ],
)
def get_branch_catalog(
    branch_unique_id: str,
    db: DBSession,
    current_user=Depends(
            require_roles(
                CUSTOMER,
                SUPER_ADMIN,
                BRANCH_MANAGER,
            )
        ),
):
    return (
        branch_catalog_service
        .get_branch_catalog(
            db=db,
            branch_unique_id=branch_unique_id,
        )
    )