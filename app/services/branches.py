from sqlalchemy.orm import Session

from app.models.branches_model import Branch
from app.schemas.branch_schema import (
    BranchCreate,
    BranchUpdate,
)

from app.exceptions.custom_exceptions import (
    ConflictException,
    NotFoundException,
)

from app.exceptions import messages as msg


class BranchService:

    def create_branch(
        self,
        db: Session,
        branch: BranchCreate,
    ):
        """Create a new branch."""

        existing_branch = (
            db.query(Branch)
            .filter(
                Branch.name == branch.name,
                Branch.city == branch.city,
            )
            .first()
        )

        if existing_branch:
            raise ConflictException(
                msg.BRANCH_ALREADY_EXISTS
            )

        new_branch = Branch(
            name=branch.name,
            address=branch.address,
            city=branch.city,
            pincode=branch.pincode,
        )

        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)

        return new_branch


    def get_branch(
        self,
        db: Session,
        unique_id: str,
    ):
        """Get a branch using its public unique ID."""

        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id == unique_id
            )
            .first()
        )

        if not branch:
            raise NotFoundException(
                msg.BRANCH_NOT_FOUND
            )

        return branch


    def update_branch(
        self,
        db: Session,
        unique_id: str,
        branch_data: BranchUpdate,
    ):
        """Update branch information."""

        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id == unique_id
            )
            .first()
        )

        if not branch:
            raise NotFoundException(
                msg.BRANCH_NOT_FOUND
            )

        update_data = branch_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(branch, field, value)

        db.commit()
        db.refresh(branch)

        return branch


    def get_all_branches(
        self,
        db: Session,
    ):
        """Return all branches."""

        branches = db.query(Branch).all()

        return branches




    def delete_branch(
        self,
        db: Session,
        unique_id: str,
    ):
        """Delete a branch."""

        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id == unique_id
            )
            .first()
        )

        if not branch:
            raise NotFoundException(
                msg.BRANCH_NOT_FOUND
            )

        response = {
            "unique_id": branch.unique_id,
            "name": branch.name,
            "message": "Branch deleted successfully.",
        }

        db.delete(branch)
        db.commit()

        return response