from sqlalchemy.orm import Session

from  app.models.branchmanager_model import BranchManager

from  app.schemas.branchmanager_schema import (
    BranchManagerCreate,
    BranchManagerUpdate,
)

from  app.core.security import hash_password

from  app.exceptions.custom_exceptions import (
    ConflictException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class BranchManagerService:

    def create_branch_manager(
        self,
        db: Session,
        manager: BranchManagerCreate,
    ):
        """
        Create a new Branch Manager.

        The manager is created without assigning a branch.
        Branch assignment is handled separately from the Branch service.
        """

        # Check whether a manager with the same email already exists.
        existing_manager = (
            db.query(BranchManager)
            .filter(
                BranchManager.email == manager.email
            )
            .first()
        )

        if existing_manager:
            raise ConflictException(
                msg.BRANCH_MANAGER_ALREADY_EXISTS
            )

        # Create the manager without a branch assignment.
        new_manager = BranchManager(
            name=manager.name,
            email=manager.email,
            password_hash=hash_password(
                manager.password
            ),
        )

        db.add(new_manager)
        db.commit()
        db.refresh(new_manager)

        return new_manager


    def get_branch_manager(
        self,
        db: Session,
        unique_id: str,
    ):
        """
        Return one Branch Manager using the public unique ID.

        If a branch is assigned, the relationship can be accessed
        through manager.branch.
        """

        manager = (
            db.query(BranchManager)
            .filter(
                BranchManager.unique_id == unique_id
            )
            .first()
        )

        if not manager:
            raise NotFoundException(
                msg.BRANCH_MANAGER_NOT_FOUND
            )

        return manager


    def get_all_branch_managers(
        self,
        db: Session,
    ):
        """Return all Branch Managers."""

        return db.query(BranchManager).all()


    def update_branch_manager(
        self,
        db: Session,
        unique_id: str,
        manager_data: BranchManagerUpdate,
    ):
        """
        Update Branch Manager information.

        Only the fields provided in the request body are updated.
        Branch assignment is not handled here.
        """

        manager = (
            db.query(BranchManager)
            .filter(
                BranchManager.unique_id == unique_id
            )
            .first()
        )

        if not manager:
            raise NotFoundException(
                msg.BRANCH_MANAGER_NOT_FOUND
            )

        update_data = manager_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                manager,
                field,
                value
            )

        db.commit()
        db.refresh(manager)

        return manager


    def delete_branch_manager(
        self,
        db: Session,
        unique_id: str,
    ):
        """
        Delete a Branch Manager.

        If the manager is assigned to a branch, the relationship
        is removed automatically when the manager row is deleted.
        """

        manager = (
            db.query(BranchManager)
            .filter(
                BranchManager.unique_id == unique_id
            )
            .first()
        )

        if not manager:
            raise NotFoundException(
                msg.BRANCH_MANAGER_NOT_FOUND
            )

        response = {
            "unique_id": manager.unique_id,
            "name": manager.name,
            "message": "Branch Manager deleted successfully.",
        }

        db.delete(manager)
        db.commit()

        return response