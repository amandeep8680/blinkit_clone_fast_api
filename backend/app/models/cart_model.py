from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from  app.database.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Cart is connected to one branch because
    # inventory/stock is branch specific.
    branch_id = Column(
        Integer,
        ForeignKey(
            "branches.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
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

    customer = relationship(
        "Customer",
        back_populates="carts",
    )

    branch = relationship(
        "Branch",
        back_populates="carts",
    )

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )


       

class CartItem(Base):
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_variant_id",
            name="uq_cart_product_variant",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    cart_id = Column(
        Integer,
        ForeignKey(
            "carts.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_variant_id = Column(
        Integer,
        ForeignKey(
            "product_variants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1,
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

    cart = relationship(
        "Cart",
        back_populates="items",
    )

    product_variant = relationship(
        "ProductVariant",
        back_populates="cart_items",
    )

 