from sqlalchemy.orm import Session

from  app.models.branches_model import Branch
from  app.models.product_variant_model import ProductVariant
from  app.models.branch_inventory_model import BranchInventory

from  app.schemas.branch_inventory_schema import (
    BranchInventoryCreate,
    BranchInventoryUpdate,
)

from  app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class BranchInventoryService:

    def create_inventory(self, db: Session, data: BranchInventoryCreate):
        """
        Create inventory for a product variant inside a branch.
        """

        branch = (
            db.query(Branch)
            .filter(Branch.unique_id == data.branch_unique_id)
            .first()
        )

        if not branch:
            raise NotFoundException(msg.BRANCH_NOT_FOUND)

        variant = (
            db.query(ProductVariant)
            .filter(ProductVariant.unique_id == data.product_variant_unique_id)
            .first()
        )

        if not variant:
            raise NotFoundException(msg.PRODUCT_VARIANT_NOT_FOUND)

        existing_inventory = (
            db.query(BranchInventory)
            .filter(
                BranchInventory.branch_id == branch.id,
                BranchInventory.product_variant_id == variant.id,
            )
            .first()
        )

        if existing_inventory:
            raise ConflictException(msg.INVENTORY_ALREADY_EXISTS)

        inventory = BranchInventory(
            branch_id=branch.id,
            product_variant_id=variant.id,
            stock_quantity=data.stock_quantity,
            selling_price_override=data.selling_price_override,
            is_available=data.is_available,
        )

        db.add(inventory)
        db.commit()
        db.refresh(inventory)

        return inventory


    def get_inventory(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
    ):
        """
        Get one inventory record using branch + product variant.
        """

        inventory = (
            db.query(BranchInventory)
            .join(Branch, BranchInventory.branch_id == Branch.id)
            .join(
                ProductVariant,
                BranchInventory.product_variant_id == ProductVariant.id,
            )
            .filter(
                Branch.unique_id == branch_unique_id,
                ProductVariant.unique_id == product_variant_unique_id,
            )
            .first()
        )

        if not inventory:
            raise NotFoundException(msg.INVENTORY_NOT_FOUND)

        return inventory


    def get_all_inventory(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Return all inventory records.
        """

        return (
            db.query(BranchInventory)
            .order_by(BranchInventory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_inventory_by_branch(
        self,
        db: Session,
        branch_unique_id: str,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Return all inventory records belonging to one branch.
        """

        branch = (
            db.query(Branch)
            .filter(Branch.unique_id == branch_unique_id)
            .first()
        )

        if not branch:
            raise NotFoundException(msg.BRANCH_NOT_FOUND)

        return (
            db.query(BranchInventory)
            .filter(BranchInventory.branch_id == branch.id)
            .order_by(BranchInventory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


    def update_inventory(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
        data: BranchInventoryUpdate,
    ):
        """
        Update stock, price override or availability.
        """

        inventory = self.get_inventory(
            db,
            branch_unique_id,
            product_variant_unique_id,
        )

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(inventory, field, value)

        db.commit()
        db.refresh(inventory)

        return inventory


    def increase_stock(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
        quantity: int,
    ):
        """
        Increase stock quantity.
        """

        if quantity <= 0:
            raise BadRequestException(msg.INVALID_STOCK_QUANTITY)

        inventory = self.get_inventory(
            db,
            branch_unique_id,
            product_variant_unique_id,
        )

        inventory.stock_quantity += quantity

        db.commit()
        db.refresh(inventory)

        return inventory


    def decrease_stock(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
        quantity: int,
    ):
        """
        Decrease stock without allowing negative stock.
        """

        if quantity <= 0:
            raise BadRequestException(msg.INVALID_STOCK_QUANTITY)

        inventory = self.get_inventory(
            db,
            branch_unique_id,
            product_variant_unique_id,
        )

        if inventory.stock_quantity < quantity:
            raise BadRequestException(msg.INSUFFICIENT_STOCK)

        inventory.stock_quantity -= quantity

        db.commit()
        db.refresh(inventory)

        return inventory


    def activate_inventory(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
    ):
        """
        Mark inventory item as available.
        """

        inventory = self.get_inventory(
            db,
            branch_unique_id,
            product_variant_unique_id,
        )

        if inventory.is_available:
            raise BadRequestException(msg.INVENTORY_ALREADY_ACTIVE)

        inventory.is_available = True

        db.commit()
        db.refresh(inventory)

        return inventory


    def deactivate_inventory(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
    ):
        """
        Mark inventory item as unavailable.
        """

        inventory = self.get_inventory(
            db,
            branch_unique_id,
            product_variant_unique_id,
        )

        if not inventory.is_available:
            raise BadRequestException(msg.INVENTORY_ALREADY_INACTIVE)

        inventory.is_available = False

        db.commit()
        db.refresh(inventory)

        return inventory


    def delete_inventory(
        self,
        db: Session,
        branch_unique_id: str,
        product_variant_unique_id: str,
    ):
        """
        Permanently delete inventory record.
        """

        inventory = self.get_inventory(
            db,
            branch_unique_id,
            product_variant_unique_id,
        )

        db.delete(inventory)
        db.commit()

        return {"message": msg.INVENTORY_DELETED}