import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


# =========================================================
# Order
# =========================================================

class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    unique_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    branch_id = Column(
        Integer,
        ForeignKey(
            "branches.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    # -------------------------
    # Address Snapshot
    # -------------------------
    # Address ka snapshot save karenge.
    # Customer future me saved address edit/delete kare
    # tab bhi old order address same rahega.

    address_label = Column(
        String,
        nullable=False,
    )

    address_line = Column(
        String,
        nullable=False,
    )

    landmark = Column(
        String,
        nullable=True,
    )

    city = Column(
        String,
        nullable=False,
    )

    state = Column(
        String,
        nullable=False,
    )

    pincode = Column(
        String,
        nullable=False,
    )

    # -------------------------
    # Amount
    # -------------------------

    subtotal = Column(
        Numeric(12, 2),
        nullable=False,
    )

    delivery_charge = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    discount_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    total_amount = Column(
        Numeric(12, 2),
        nullable=False,
    )

    # -------------------------
    # Order / Payment Status
    # -------------------------

    status = Column(
        String,
        nullable=False,
        default="placed",
        index=True,
    )

    payment_method = Column(
        String,
        nullable=False,
        default="cod",
    )

    payment_status = Column(
        String,
        nullable=False,
        default="pending",
    )

    customer_note = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # -------------------------
    # Relationships
    # -------------------------

    customer = relationship(
        "Customer",
        back_populates="orders",
    )

    branch = relationship(
        "Branch",
        back_populates="orders",
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    history = relationship(
        "OrderHistory",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderHistory.created_at",
    )


# =========================================================
# Order Item
# =========================================================

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_variant_id = Column(
        Integer,
        ForeignKey(
            "product_variants.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    # Product snapshot
    product_name = Column(
        String,
        nullable=False,
    )

    variant_value = Column(
        String,
        nullable=False,
    )

    variant_unit = Column(
        String,
        nullable=False,
    )

    sku = Column(
        String,
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
    )

    mrp = Column(
        Numeric(12, 2),
        nullable=False,
    )

    unit_price = Column(
        Numeric(12, 2),
        nullable=False,
    )

    total_price = Column(
        Numeric(12, 2),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    order = relationship(
        "Order",
        back_populates="items",
    )

    product_variant = relationship(
        "ProductVariant",
        back_populates="order_items",
    )


# =========================================================
# Order History
# =========================================================

class OrderHistory(Base):
    __tablename__ = "order_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        index=True,
    )

    note = Column(
        Text,
        nullable=True,
    )

    changed_by_unique_id = Column(
        String,
        nullable=False,
    )

    changed_by_role = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    order = relationship(
        "Order",
        back_populates="history",
    )