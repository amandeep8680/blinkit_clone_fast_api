from sqlalchemy.orm import Session

from  app.models.branches_model import Branch
from  app.models.branchmanager_model import BranchManager

from  app.schemas.branch_schema import (
    BranchCreate,
    BranchUpdate,
    BranchManagerAssign,
)

from  app.exceptions.custom_exceptions import (
    ConflictException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class BranchService:

    def create_branch(
        self,
        db: Session,
        branch: BranchCreate,
    ):
        """
        Create a new branch.

        A branch is considered duplicate when another branch
        with the same name and city already exists.
        """

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
        """
        Return a branch using its public unique ID.
        """

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


    def get_all_branches(
        self,
        db: Session,
    ):
        """
        Return all branches.
        """

        return db.query(Branch).all()


    def update_branch(
        self,
        db: Session,
        unique_id: str,
        branch_data: BranchUpdate,
    ):
        """
        Update branch information.

        Only the fields provided in the request body
        will be updated.
        """

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
            setattr(
                branch,
                field,
                value
            )

        db.commit()
        db.refresh(branch)

        return branch


    def assign_branch_manager(
        self,
        db: Session,
        branch_unique_id: str,
        manager_data: BranchManagerAssign,
    ):
        """
        Assign or change the manager of a branch.

        The branch is identified using its public unique ID.
        The manager is also identified using a public unique ID.

        If the branch already has a manager, the old manager
        is unassigned before the new manager is assigned.
        """

        # Find the branch that needs a manager.
        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id == branch_unique_id
            )
            .first()
        )

        if not branch:
            raise NotFoundException(
                msg.BRANCH_NOT_FOUND
            )

        # Find the manager that should be assigned.
        manager = (
            db.query(BranchManager)
            .filter(
                BranchManager.unique_id
                == manager_data.manager_unique_id
            )
            .first()
        )

        if not manager:
            raise NotFoundException(
                msg.BRANCH_MANAGER_NOT_FOUND
            )

        # Prevent assigning the same manager again.
        if branch.manager and branch.manager.id == manager.id:
            raise ConflictException(
                "This manager is already assigned to this branch."
            )

        # A manager can only manage one branch.
        if manager.branch_id is not None:
            raise ConflictException(
                "This manager is already assigned to another branch."
            )

        # If this branch already has a manager,
        # remove the previous assignment first.
        if branch.manager:
            branch.manager.branch_id = None

        # Assign the new manager using the internal branch ID.
        manager.branch_id = branch.id

        db.commit()

        # Refresh both objects so the latest relationship
        # is available in the returned branch object.
        db.refresh(branch)
        db.refresh(manager)

        return branch


    def delete_branch(
        self,
        db: Session,
        unique_id: str,
    ):
        """
        Delete a branch.

        If a manager is currently assigned to the branch,
        the manager is first unassigned so that the manager
        record can continue to exist independently.
        """

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

        # Unassign the manager before deleting the branch.
        if branch.manager:
            branch.manager.branch_id = None

        response = {
            "unique_id": branch.unique_id,
            "name": branch.name,
            "message": "Branch deleted successfully.",
        }

        db.delete(branch)
        db.commit()

        return response