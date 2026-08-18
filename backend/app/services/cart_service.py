from sqlalchemy.orm import Session

from  app.models.cart_model import (
    Cart,
    CartItem,
)

from  app.models.branches_model import Branch
from  app.models.product_variant_model import ProductVariant
from  app.models.branch_inventory_model import BranchInventory

from  app.schemas.cart_schema import (
    CartCreate,
    CartItemCreate,
    CartItemUpdate,
)

from  app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class CartService:

    # =====================================================
    # Create Cart
    # =====================================================

    def create_cart(self, db: Session, customer, data: CartCreate):
        """
        Create one active cart for logged-in customer.
        """

        existing_cart = (
            db.query(Cart)
            .filter(
                Cart.customer_id == customer.id,
                Cart.is_active.is_(True),
            )
            .first()
        )

        if existing_cart:
            raise ConflictException(
                msg.CART_ALREADY_EXISTS
            )

        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id == data.branch_unique_id
            )
            .first()
        )

        if not branch:
            raise NotFoundException(
                msg.BRANCH_NOT_FOUND
            )

        if not branch.is_active:
            raise BadRequestException(
                msg.BRANCH_INACTIVE
            )

        cart = Cart(
            customer_id=customer.id,
            branch_id=branch.id,
            is_active=True,
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

        return cart


    # =====================================================
    # Get Active Cart
    # =====================================================

    def get_active_cart(self, db: Session, customer):
        cart = (
            db.query(Cart)
            .filter(
                Cart.customer_id == customer.id,
                Cart.is_active.is_(True),
            )
            .first()
        )

        if not cart:
            raise NotFoundException(
                msg.CART_NOT_FOUND
            )

        return cart


    # =====================================================
    # Add Item
    # =====================================================

    def add_item(self, db: Session, customer, data: CartItemCreate):
        """
        Add ProductVariant to active cart.

        If item already exists, increase its quantity.
        """

        cart = self.get_active_cart(
            db,
            customer,
        )

        variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.unique_id
                == data.product_variant_unique_id
            )
            .first()
        )

        if not variant:
            raise NotFoundException(
                msg.PRODUCT_VARIANT_NOT_FOUND
            )

        if not variant.is_active:
            raise BadRequestException(
                msg.PRODUCT_VARIANT_INACTIVE
            )

        # Find variant inventory inside cart branch.
        inventory = (
            db.query(BranchInventory)
            .filter(
                BranchInventory.branch_id == cart.branch_id,
                BranchInventory.product_variant_id == variant.id,
            )
            .first()
        )

        if not inventory or not inventory.is_available:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        existing_item = (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id,
                CartItem.product_variant_id == variant.id,
            )
            .first()
        )

        if existing_item:
            new_quantity = (
                existing_item.quantity
                + data.quantity
            )

            if new_quantity > inventory.stock_quantity:
                raise BadRequestException(
                    msg.CART_QUANTITY_EXCEEDS_STOCK
                )

            existing_item.quantity = new_quantity

            db.commit()
            db.refresh(existing_item)

            return existing_item

        if data.quantity > inventory.stock_quantity:
            raise BadRequestException(
                msg.CART_QUANTITY_EXCEEDS_STOCK
            )

        cart_item = CartItem(
            cart_id=cart.id,
            product_variant_id=variant.id,
            quantity=data.quantity,
        )

        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

        return cart_item


    # =====================================================
    # Update Cart Item Quantity
    # =====================================================

    def update_item(
        self,
        db: Session,
        customer,
        product_variant_unique_id: str,
        data: CartItemUpdate,
    ):
        cart = self.get_active_cart(
            db,
            customer,
        )

        variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.unique_id
                == product_variant_unique_id
            )
            .first()
        )

        if not variant:
            raise NotFoundException(
                msg.PRODUCT_VARIANT_NOT_FOUND
            )

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id,
                CartItem.product_variant_id == variant.id,
            )
            .first()
        )

        if not cart_item:
            raise NotFoundException(
                msg.CART_ITEM_NOT_FOUND
            )

        inventory = (
            db.query(BranchInventory)
            .filter(
                BranchInventory.branch_id == cart.branch_id,
                BranchInventory.product_variant_id == variant.id,
            )
            .first()
        )

        if not inventory or not inventory.is_available:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        if data.quantity > inventory.stock_quantity:
            raise BadRequestException(
                msg.CART_QUANTITY_EXCEEDS_STOCK
            )

        cart_item.quantity = data.quantity

        db.commit()
        db.refresh(cart_item)

        return cart_item


    # =====================================================
    # Remove Cart Item
    # =====================================================

    def remove_item(
        self,
        db: Session,
        customer,
        product_variant_unique_id: str,
    ):
        cart = self.get_active_cart(
            db,
            customer,
        )

        variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.unique_id
                == product_variant_unique_id
            )
            .first()
        )

        if not variant:
            raise NotFoundException(
                msg.PRODUCT_VARIANT_NOT_FOUND
            )

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id,
                CartItem.product_variant_id == variant.id,
            )
            .first()
        )

        if not cart_item:
            raise NotFoundException(
                msg.CART_ITEM_NOT_FOUND
            )

        db.delete(cart_item)
        db.commit()

        return {
            "message": msg.CART_ITEM_DELETED
        }


    # =====================================================
    # Clear Cart
    # =====================================================

    def clear_cart(self, db: Session, customer):
        cart = self.get_active_cart(
            db,
            customer,
        )

        (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()

        return {
            "message": msg.CART_CLEARED
        }


    # =====================================================
    # Delete Cart
    # =====================================================

    def delete_cart(self, db: Session, customer):
        cart = self.get_active_cart(
            db,
            customer,
        )

        db.delete(cart)
        db.commit()

        return {
            "message": msg.CART_DELETED
        }