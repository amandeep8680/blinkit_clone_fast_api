from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order_model import (
    Order,
    OrderItem,
    OrderHistory,
)

from app.models.cart_model import (
    Cart,
    CartItem,
)

from app.models.customer_model import (
    CustomerAddress,
)

from app.models.branch_inventory_model import (
    BranchInventory,
)

from app.models.product_variant_model import (
    ProductVariant,
)

from app.models.product_model import Product

from app.schemas.order_schema import (
    OrderCreate,
    OrderStatusUpdate,
    PaymentStatusUpdate,
)

from app.constants import roles

from app.constants.order_status import (
    ORDER_PLACED,
    ORDER_CONFIRMED,
    ORDER_PACKING,
    ORDER_OUT_FOR_DELIVERY,
    ORDER_DELIVERED,
    ORDER_CANCELLED,
    ORDER_STATUSES,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
    ForbiddenException,
)

from app.exceptions import messages as msg


class OrderService:

    # =====================================================
    # Get Customer Active Cart
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
    # Get Order
    # =====================================================

    def get_order(self, db: Session, order_unique_id: str):
        order = (
            db.query(Order)
            .filter(
                Order.unique_id == order_unique_id
            )
            .first()
        )

        if not order:
            raise NotFoundException(
                msg.ORDER_NOT_FOUND
            )

        return order


    # =====================================================
    # Place Order
    # =====================================================

    def create_order(
        self,
        db: Session,
        customer,
        data: OrderCreate,
    ):
        """
        Checkout customer active cart.

        Steps:
        1. Find active cart
        2. Validate address
        3. Validate every cart item
        4. Validate branch stock
        5. Calculate prices
        6. Create Order
        7. Create OrderItems
        8. Reduce stock
        9. Add OrderHistory
        10. Close Cart
        """

        cart = self.get_active_cart(
            db,
            customer,
        )

        if not cart.items:
            raise BadRequestException(
                msg.ORDER_EMPTY_CART
            )

        if not cart.branch.is_active:
            raise BadRequestException(
                msg.ORDER_BRANCH_INACTIVE
            )

        # -----------------------------------
        # Customer Address
        # -----------------------------------

        address = (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.unique_id
                == data.address_unique_id,

                CustomerAddress.customer_id
                == customer.id,

                CustomerAddress.is_active
                .is_(True),
            )
            .first()
        )

        if not address:
            raise NotFoundException(
                msg.ORDER_ADDRESS_NOT_FOUND
            )

        # -----------------------------------
        # Payment method validation
        # -----------------------------------

        allowed_payment_methods = (
            "cod",
            "online",
        )

        if data.payment_method not in allowed_payment_methods:
            raise BadRequestException(
                msg.INVALID_PAYMENT_METHOD
            )

        subtotal = Decimal("0.00")

        order_item_data = []

        # -----------------------------------
        # Validate Cart Items
        # -----------------------------------

        for cart_item in cart.items:

            variant = cart_item.product_variant
            product = variant.product

            if not variant.is_active or not product.is_active:
                raise BadRequestException(
                    msg.ORDER_ITEM_NOT_AVAILABLE
                )

            inventory = (
                db.query(BranchInventory)
                .filter(
                    BranchInventory.branch_id
                    == cart.branch_id,

                    BranchInventory.product_variant_id
                    == variant.id,
                )
                .with_for_update()
                .first()
            )

            if (
                not inventory
                or not inventory.is_available
            ):
                raise BadRequestException(
                    msg.ORDER_ITEM_NOT_AVAILABLE
                )

            if inventory.stock_quantity < cart_item.quantity:
                raise BadRequestException(
                    msg.ORDER_ITEM_OUT_OF_STOCK
                )

            unit_price = (
                inventory.selling_price_override
                if inventory.selling_price_override
                is not None
                else variant.selling_price
            )

            item_total = (
                unit_price
                * cart_item.quantity
            )

            subtotal += item_total

            order_item_data.append(
                {
                    "variant": variant,
                    "inventory": inventory,
                    "quantity": cart_item.quantity,
                    "unit_price": unit_price,
                    "item_total": item_total,
                }
            )

        # For now zero.
        # Later delivery charge service/coupon system add kar sakte ho.
        delivery_charge = Decimal("0.00")
        discount_amount = Decimal("0.00")

        total_amount = (
            subtotal
            + delivery_charge
            - discount_amount
        )

        try:

            # -----------------------------------
            # Create Order
            # -----------------------------------

            order = Order(
                customer_id=customer.id,
                branch_id=cart.branch_id,

                address_label=address.label,
                address_line=address.address_line,
                landmark=address.landmark,
                city=address.city,
                state=address.state,
                pincode=address.pincode,

                subtotal=subtotal,
                delivery_charge=delivery_charge,
                discount_amount=discount_amount,
                total_amount=total_amount,

                status=ORDER_PLACED,

                payment_method=data.payment_method,

                payment_status=(
                    "pending"
                    if data.payment_method == "online"
                    else "pending"
                ),

                customer_note=data.customer_note,
            )

            db.add(order)
            db.flush()

            # -----------------------------------
            # Create Order Items + Reduce Stock
            # -----------------------------------

            for item in order_item_data:

                variant = item["variant"]
                inventory = item["inventory"]

                product = variant.product

                order_item = OrderItem(
                    order_id=order.id,
                    product_variant_id=variant.id,

                    product_name=product.name,

                    variant_value=variant.value,
                    variant_unit=variant.unit,
                    sku=variant.sku,

                    quantity=item["quantity"],

                    mrp=variant.mrp,
                    unit_price=item["unit_price"],
                    total_price=item["item_total"],
                )

                db.add(order_item)

                inventory.stock_quantity -= (
                    item["quantity"]
                )

            # -----------------------------------
            # Order History
            # -----------------------------------

            history = OrderHistory(
                order_id=order.id,
                status=ORDER_PLACED,
                note="Order placed by customer.",
                changed_by_unique_id=customer.unique_id,
                changed_by_role=customer.role,
            )

            db.add(history)

            # -----------------------------------
            # Close Cart
            # -----------------------------------

            cart.is_active = False

            db.commit()
            db.refresh(order)

            return order

        except Exception:
            db.rollback()
            raise


    # =====================================================
    # Get My Orders
    # =====================================================

    def get_customer_orders(
        self,
        db: Session,
        customer,
        skip: int = 0,
        limit: int = 100,
    ):
        return (
            db.query(Order)
            .filter(
                Order.customer_id == customer.id
            )
            .order_by(
                Order.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    # =====================================================
    # Get Customer Order Detail
    # =====================================================

    def get_customer_order(
        self,
        db: Session,
        customer,
        order_unique_id: str,
    ):
        order = (
            db.query(Order)
            .filter(
                Order.unique_id == order_unique_id,
                Order.customer_id == customer.id,
            )
            .first()
        )

        if not order:
            raise NotFoundException(
                msg.ORDER_NOT_FOUND
            )

        return order


    # =====================================================
    # Get All Orders - Admin/Manager
    # =====================================================

    def get_all_orders(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return (
            db.query(Order)
            .order_by(
                Order.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    # =====================================================
    # Get Branch Orders
    # =====================================================

    def get_branch_orders(
        self,
        db: Session,
        branch_id: int,
        skip: int = 0,
        limit: int = 100,
    ):
        return (
            db.query(Order)
            .filter(
                Order.branch_id == branch_id
            )
            .order_by(
                Order.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    # =====================================================
    # Cancel Order - Customer
    # =====================================================

    def cancel_order(
        self,
        db: Session,
        customer,
        order_unique_id: str,
    ):
        order = self.get_customer_order(
            db,
            customer,
            order_unique_id,
        )

        if order.status == ORDER_CANCELLED:
            raise BadRequestException(
                msg.ORDER_ALREADY_CANCELLED
            )

        if order.status in (
            ORDER_OUT_FOR_DELIVERY,
            ORDER_DELIVERED,
        ):
            raise BadRequestException(
                msg.ORDER_CANNOT_CANCEL
            )

        # Restore inventory stock.
        for item in order.items:

            inventory = (
                db.query(BranchInventory)
                .filter(
                    BranchInventory.branch_id
                    == order.branch_id,

                    BranchInventory.product_variant_id
                    == item.product_variant_id,
                )
                .with_for_update()
                .first()
            )

            if inventory:
                inventory.stock_quantity += (
                    item.quantity
                )

        order.status = ORDER_CANCELLED

        history = OrderHistory(
            order_id=order.id,
            status=ORDER_CANCELLED,
            note="Order cancelled by customer.",
            changed_by_unique_id=customer.unique_id,
            changed_by_role=customer.role,
        )

        db.add(history)

        db.commit()
        db.refresh(order)

        return order


    # =====================================================
    # Update Order Status
    # =====================================================

    def update_order_status(
        self,
        db: Session,
        current_user,
        order_unique_id: str,
        data: OrderStatusUpdate,
    ):
        order = self.get_order(
            db,
            order_unique_id,
        )

        if data.status not in ORDER_STATUSES:
            raise BadRequestException(
                msg.INVALID_ORDER_STATUS
            )

        if order.status == ORDER_CANCELLED:
            raise BadRequestException(
                msg.ORDER_ALREADY_CANCELLED
            )

        if order.status == ORDER_DELIVERED:
            raise BadRequestException(
                msg.ORDER_ALREADY_DELIVERED
            )

        # Allowed status flow
        allowed_transitions = {
            ORDER_PLACED: (
                ORDER_CONFIRMED,
                ORDER_CANCELLED,
            ),

            ORDER_CONFIRMED: (
                ORDER_PACKING,
                ORDER_CANCELLED,
            ),

            ORDER_PACKING: (
                ORDER_OUT_FOR_DELIVERY,
                ORDER_CANCELLED,
            ),

            ORDER_OUT_FOR_DELIVERY: (
                ORDER_DELIVERED,
            ),
        }

        valid_next_statuses = (
            allowed_transitions.get(
                order.status,
                (),
            )
        )

        if data.status not in valid_next_statuses:
            raise BadRequestException(
                msg.INVALID_ORDER_STATUS_TRANSITION
            )

        # If admin/manager cancels,
        # restore stock.
        if data.status == ORDER_CANCELLED:

            for item in order.items:

                inventory = (
                    db.query(BranchInventory)
                    .filter(
                        BranchInventory.branch_id
                        == order.branch_id,

                        BranchInventory.product_variant_id
                        == item.product_variant_id,
                    )
                    .with_for_update()
                    .first()
                )

                if inventory:
                    inventory.stock_quantity += (
                        item.quantity
                    )

        order.status = data.status

        history = OrderHistory(
            order_id=order.id,
            status=data.status,
            note=data.note,
            changed_by_unique_id=current_user.unique_id,
            changed_by_role=current_user.role,
        )

        db.add(history)

        db.commit()
        db.refresh(order)

        return order


    # =====================================================
    # Update Payment Status
    # =====================================================

    def update_payment_status(
        self,
        db: Session,
        order_unique_id: str,
        data: PaymentStatusUpdate,
    ):
        order = self.get_order(
            db,
            order_unique_id,
        )

        valid_statuses = (
            "pending",
            "paid",
            "failed",
            "refunded",
        )

        if data.payment_status not in valid_statuses:
            raise BadRequestException(
                msg.INVALID_PAYMENT_STATUS
            )

        order.payment_status = (
            data.payment_status
        )

        db.commit()
        db.refresh(order)

        return order