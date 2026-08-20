# app/services/cart_service.py

from sqlalchemy.orm import Session

from app.models.cart_model import (
    Cart,
    CartItem,
)

from app.models.branches_model import Branch
from app.models.product_variant_model import ProductVariant
from app.models.branch_inventory_model import BranchInventory

from app.schemas.cart_schema import (
    CartCreate,
    CartItemCreate,
    CartItemUpdate,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from app.realtime.cart_subscription import (
    publish_cart_subscription_change,
)

from app.exceptions import messages as msg


class CartService:

    # =====================================================
    # Create Cart
    # =====================================================

    def create_cart(
        self,
        db: Session,
        customer,
        data: CartCreate,
    ):
        """
        Create one active cart for logged-in customer.
        """

        # Customer can have only one active cart.
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

        # Find selected branch.
        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id
                == data.branch_unique_id
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
    # FIND ACTIVE CART
    # =====================================================

    def find_active_cart(
        self,
        db: Session,
        customer,
    ):
        """
        Return actual SQLAlchemy Cart object.

        Use this method inside:
        - add_item
        - update_item
        - remove_item
        - clear_cart
        - delete_cart
        - order checkout
        """

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
    # Build Cart Item API Response
    # =====================================================

    def build_cart_item_response(
        self,
        db: Session,
        cart: Cart,
        cart_item: CartItem,
    ):
        """
        Build one cart item response with:
        - latest stock
        - availability
        - availability message
        - branch-specific selling price
        """

        variant = cart_item.product_variant
        product = variant.product

        # Find current inventory for this variant
        # inside selected cart branch.
        inventory = (
            db.query(BranchInventory)
            .filter(
                BranchInventory.branch_id
                == cart.branch_id,

                BranchInventory.product_variant_id
                == variant.id,
            )
            .first()
        )

        is_available = True
        available_stock = 0
        availability_message = None

        # -----------------------------------
        # Inventory Missing
        # -----------------------------------

        if not inventory:
            is_available = False

            availability_message = (
                "Product is not available in this branch."
            )

        else:
            available_stock = (
                inventory.stock_quantity
            )

            # -----------------------------------
            # Inventory manually unavailable
            # -----------------------------------

            if not inventory.is_available:
                is_available = False

                availability_message = (
                    "Product is currently unavailable."
                )

            # -----------------------------------
            # Product Variant inactive
            # -----------------------------------

            elif not variant.is_active:
                is_available = False

                availability_message = (
                    "Product variant is currently unavailable."
                )

            # -----------------------------------
            # Parent Product inactive
            # -----------------------------------

            elif not product.is_active:
                is_available = False

                availability_message = (
                    "Product is currently unavailable."
                )

            # -----------------------------------
            # Completely Out Of Stock
            # -----------------------------------

            elif inventory.stock_quantity <= 0:
                is_available = False

                availability_message = (
                    "Out of stock."
                )

            # -----------------------------------
            # Stock less than Cart quantity
            # -----------------------------------

            elif (
                inventory.stock_quantity
                < cart_item.quantity
            ):
                is_available = False

                availability_message = (
                    f"Only {inventory.stock_quantity} "
                    "item(s) available."
                )

        # -----------------------------------
        # Current Selling Price
        # -----------------------------------

        selling_price = (
            variant.selling_price
        )

        # Branch price override gets priority.
        if (
            inventory
            and inventory.selling_price_override
            is not None
        ):
            selling_price = (
                inventory.selling_price_override
            )

        return {
            "quantity": cart_item.quantity,

            "is_available": is_available,

            "available_stock": available_stock,

            "availability_message": (
                availability_message
            ),

            "product_variant": {
                "unique_id": variant.unique_id,
                "sku": variant.sku,
                "value": variant.value,
                "unit": variant.unit,
                "mrp": variant.mrp,
                "selling_price": selling_price,
            },

            "created_at": cart_item.created_at,
            "updated_at": cart_item.updated_at,
        }


    # =====================================================
    # Get Active Cart
    # =====================================================

    def get_active_cart(
        self,
        db: Session,
        customer,
    ):
        """
        Return customer's active cart.

        Every cart item is checked against
        latest branch inventory when cart loads.
        """

        cart = self.find_active_cart(
            db,
            customer,
        )

        items = [
            self.build_cart_item_response(
                db,
                cart,
                cart_item,
            )
            for cart_item in cart.items
        ]

        # Checkout allowed only when:
        # - cart contains at least one item
        # - every item is currently available
        can_checkout = (
            len(items) > 0
            and all(
                item["is_available"]
                for item in items
            )
        )

        return {
            "is_active": cart.is_active,

            "can_checkout": can_checkout,

            "branch": {
                "unique_id": cart.branch.unique_id,
                "name": cart.branch.name,
                "city": cart.branch.city,
            },

            "items": items,

            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
        }


    # =====================================================
    # Add Item
    # =====================================================

    def add_item(
        self,
        db: Session,
        customer,
        data: CartItemCreate,
    ):
        """
        Add ProductVariant to active cart.

        If same variant already exists,
        increase its quantity.
        """

        cart = self.find_active_cart(
            db,
            customer,
        )

        # -----------------------------------
        # Find Product Variant
        # -----------------------------------

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

        # -----------------------------------
        # Variant Active Check
        # -----------------------------------

        if not variant.is_active:
            raise BadRequestException(
                msg.PRODUCT_VARIANT_INACTIVE
            )

        # -----------------------------------
        # Parent Product Active Check
        # -----------------------------------

        if not variant.product.is_active:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        # -----------------------------------
        # Branch Inventory Check
        # -----------------------------------

        inventory = (
            db.query(BranchInventory)
            .filter(
                BranchInventory.branch_id
                == cart.branch_id,

                BranchInventory.product_variant_id
                == variant.id,
            )
            .first()
        )

        if not inventory:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        if not inventory.is_available:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        if inventory.stock_quantity <= 0:
            raise BadRequestException(
                msg.CART_QUANTITY_EXCEEDS_STOCK
            )

        # -----------------------------------
        # Existing Cart Item
        # -----------------------------------

        existing_item = (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id,

                CartItem.product_variant_id
                == variant.id,
            )
            .first()
        )

        # Same variant exists:
        # simply increase quantity.
        if existing_item:

            new_quantity = (
                existing_item.quantity
                + data.quantity
            )

            if (
                new_quantity
                > inventory.stock_quantity
            ):
                raise BadRequestException(
                    msg.CART_QUANTITY_EXCEEDS_STOCK
                )

            existing_item.quantity = (
                new_quantity
            )

            db.commit()
            db.refresh(existing_item)

            return self.build_cart_item_response(
                db,
                cart,
                existing_item,
            )

        # -----------------------------------
        # New Item Quantity Validation
        # -----------------------------------

        if (
            data.quantity
            > inventory.stock_quantity
        ):
            raise BadRequestException(
                msg.CART_QUANTITY_EXCEEDS_STOCK
            )

        # -----------------------------------
        # Create Cart Item
        # -----------------------------------

        cart_item = CartItem(
            cart_id=cart.id,
            product_variant_id=variant.id,
            quantity=data.quantity,
        )

        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

        # Dynamically subscribe currently-open SSE connection
        # to this newly added variant.
        publish_cart_subscription_change(
            customer_id=customer.id,
            action="subscribe",
            branch_id=cart.branch_id,
            product_variant_id=variant.id,
        )

        return self.build_cart_item_response(
            db,
            cart,
            cart_item,
        )

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
        """
        Replace current cart item quantity
        with requested quantity.
        """

        cart = self.find_active_cart(
            db,
            customer,
        )

        # -----------------------------------
        # Find Variant
        # -----------------------------------

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

        if not variant.is_active:
            raise BadRequestException(
                msg.PRODUCT_VARIANT_INACTIVE
            )

        if not variant.product.is_active:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        # -----------------------------------
        # Find Cart Item
        # -----------------------------------

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id,

                CartItem.product_variant_id
                == variant.id,
            )
            .first()
        )

        if not cart_item:
            raise NotFoundException(
                msg.CART_ITEM_NOT_FOUND
            )

        # -----------------------------------
        # Inventory Check
        # -----------------------------------

        inventory = (
            db.query(BranchInventory)
            .filter(
                BranchInventory.branch_id
                == cart.branch_id,

                BranchInventory.product_variant_id
                == variant.id,
            )
            .first()
        )

        if not inventory:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        if not inventory.is_available:
            raise BadRequestException(
                msg.PRODUCT_NOT_AVAILABLE
            )

        if inventory.stock_quantity <= 0:
            raise BadRequestException(
                msg.CART_QUANTITY_EXCEEDS_STOCK
            )

        if (
            data.quantity
            > inventory.stock_quantity
        ):
            raise BadRequestException(
                msg.CART_QUANTITY_EXCEEDS_STOCK
            )

        # -----------------------------------
        # Update Quantity
        # -----------------------------------

        cart_item.quantity = (
            data.quantity
        )

        db.commit()
        db.refresh(cart_item)

        return self.build_cart_item_response(
            db,
            cart,
            cart_item,
        )


    # =====================================================
    # Remove Cart Item
    # =====================================================

    def remove_item(
        self,
        db: Session,
        customer,
        product_variant_unique_id: str,
    ):
        """
        Remove one ProductVariant from cart.
        """

        cart = self.find_active_cart(
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

                CartItem.product_variant_id
                == variant.id,
            )
            .first()
        )

        if not cart_item:
            raise NotFoundException(
                msg.CART_ITEM_NOT_FOUND
            )

        db.delete(cart_item)
        db.commit()
        publish_cart_subscription_change(
            customer_id=customer.id,
            action="unsubscribe",
            branch_id=cart.branch_id,
            product_variant_id=variant.id,
        )
        return {
            "message": msg.CART_ITEM_DELETED
        }


    # =====================================================
    # Clear Cart
    # =====================================================

    def clear_cart(
            self,
            db: Session,
            customer,
        ):
            """
            Remove every item from active cart.

            Cart itself remains active.
            """

            cart = self.find_active_cart(
                db,
                customer,
            )

            # Save variant IDs BEFORE deleting cart items.
            variant_ids = [
                item.product_variant_id
                for item in cart.items
            ]

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

            # Remove all inventory subscriptions
            # from customer's currently-open SSE connection.
            for variant_id in variant_ids:

                publish_cart_subscription_change(
                    customer_id=customer.id,
                    action="unsubscribe",
                    branch_id=cart.branch_id,
                    product_variant_id=variant_id,
                )

            return {
                "message": msg.CART_CLEARED
            }

    # =====================================================
    # Delete Cart
    # =====================================================

    def delete_cart(
        self,
        db: Session,
        customer,
    ):
        """
        Permanently delete customer's active cart.
        """

        cart = self.find_active_cart(
            db,
            customer,
        )

        branch_id = cart.branch_id

        variant_ids = [
            item.product_variant_id
            for item in cart.items
        ]

        db.delete(cart)
        db.commit()

        for variant_id in variant_ids:

            publish_cart_subscription_change(
                customer_id=customer.id,
                action="unsubscribe",
                branch_id=branch_id,
                product_variant_id=variant_id,
            )

        return {
            "message": msg.CART_DELETED
        }