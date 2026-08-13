from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.branchmanager_schema import (
    BranchManagerCreate,
    BranchManagerResponse,
    BranchManagerUpdate,
    BranchManagerDeleteResponse,
)

from app.services.branchmanager_service import (
    BranchManagerService,
)

from app.auth.authorization import require_roles
from app.constants import roles


router = APIRouter(
    prefix="/branch-managers",
    tags=["Branch Managers"],
)


branch_manager_service = BranchManagerService()


DBSession = Annotated[
    Session,
    Depends(get_db)
]


@router.post(
    "/create",
    response_model=BranchManagerResponse,
)
def create_branch_manager(
    manager: BranchManagerCreate,
    db: DBSession,
    current_user=Depends(
        require_roles(
            roles.SUPER_ADMIN
        )
    ),
):
    """Create a new Branch Manager."""

    return branch_manager_service.create_branch_manager(
        db=db,
        manager=manager,
    )


@router.get(
    "/all",
    response_model=list[BranchManagerResponse],
)
def get_all_branch_managers(
    db: DBSession,
    current_user=Depends(
        require_roles(
            roles.SUPER_ADMIN,
            roles.BRANCH_MANAGER
        )
    ),
):
    """Return all Branch Managers."""

    return branch_manager_service.get_all_branch_managers(
        db=db
    )


@router.get(
    "/{unique_id}",
    response_model=BranchManagerResponse,
)
def get_branch_manager(
    unique_id: str,
    db: DBSession,
    current_user=Depends(
        require_roles(
            roles.SUPER_ADMIN
        )
    ),
):
    """Return Branch Manager details."""

    return branch_manager_service.get_branch_manager(
        db=db,
        unique_id=unique_id,
    )


@router.patch(
    "/{unique_id}",
    response_model=BranchManagerResponse,
)
def update_branch_manager(
    unique_id: str,
    manager: BranchManagerUpdate,
    db: DBSession,
    current_user=Depends(
        require_roles(
            roles.SUPER_ADMIN,
            roles.BRANCH_MANAGER
        )
    ),
):
    """Update Branch Manager information."""

    return branch_manager_service.update_branch_manager(
        db=db,
        unique_id=unique_id,
        manager_data=manager,
    )


@router.delete(
    "/{unique_id}",
    response_model=BranchManagerDeleteResponse,
)
def delete_branch_manager(
    unique_id: str,
    db: DBSession,
    current_user=Depends(
        require_roles(
            roles.SUPER_ADMIN
        )
    ),
):
    """Delete a Branch Manager."""

    return branch_manager_service.delete_branch_manager(
        db=db,
        unique_id=unique_id,
    )