from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.branch_schema import (
    BranchCreate,
    BranchResponse,
    BranchUpdate,
    BranchManagerAssign,
    BranchDeleteResponse,
)

from app.services.branches import BranchService

from app.auth.authorization import require_roles
from app.constants import roles
from app.models.admin_model import User


router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)


branch_service = BranchService()

DBSession = Annotated[
    Session,
    Depends(get_db)
]


@router.post(
    "/create",
    response_model=BranchResponse,
)
def create_branch(
    branch: BranchCreate,
    db: DBSession,
    current_user: User = Depends(
        require_roles(roles.SUPER_ADMIN)
    ),
):
    """Create a new branch."""

    return branch_service.create_branch(
        db=db,
        branch=branch,
    )

@router.get(
    "/",
    response_model=list[BranchResponse],
)
def get_all_branches(
    db: DBSession,
    current_user=Depends(
        require_roles(
            roles.SUPER_ADMIN,
            roles.BRANCH_MANAGER,
        )
    ),
):
    """Return all branches."""

    return branch_service.get_all_branches(
        db=db
    ) 

 
@router.get(
    "/{unique_id}",
    response_model=BranchResponse,
)
def get_branch(
    unique_id: str,
    db: DBSession,
    current_user: User = Depends(
        require_roles(roles.SUPER_ADMIN)
    ),
):
    """Get branch details."""

    return branch_service.get_branch(
        db=db,
        unique_id=unique_id,
    )



@router.patch(
    "/{unique_id}",
    response_model=BranchResponse,
)
def update_branch(
    unique_id: str,
    branch: BranchUpdate,
    db: DBSession,
    current_user: User = Depends(
        require_roles(roles.SUPER_ADMIN)
    ),
):
    """Update branch details."""

    return branch_service.update_branch(
        db=db,
        unique_id=unique_id,
        branch_data=branch,
    )


@router.delete(
    "/{unique_id}",
    response_model=BranchDeleteResponse,
)
def delete_branch(
    unique_id: str,
    db: DBSession,
    current_user: User = Depends(
        require_roles(roles.SUPER_ADMIN)
    ),
):
    """Delete a branch."""

    return branch_service.delete_branch(
        db=db,
        unique_id=unique_id,
    )


@router.patch(
    "/{branch_unique_id}/manager",
    response_model=BranchResponse,
)
def assign_branch_manager(
    branch_unique_id: str,
    manager_data: BranchManagerAssign,
    db: DBSession,
    current_user: User = Depends(
        require_roles(roles.SUPER_ADMIN)
    ),
):
    """Assign or change the manager of a branch."""

    return branch_service.assign_branch_manager(
        db=db,
        branch_unique_id=branch_unique_id,
        manager_data=manager_data,
    )