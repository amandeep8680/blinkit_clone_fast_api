# app/models/branch_inventory_model.py

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class BranchInventory(Base):
    __tablename__ = "branch_inventory"

    __table_args__ = (
        UniqueConstraint(
            "branch_id",
            "product_variant_id",
            name="uq_branch_product_variant",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    branch_id = Column(
        Integer,
        ForeignKey(
            "branches.id",
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

    stock_quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # If null, use ProductVariant.selling_price
    selling_price_override = Column(
        Numeric(10, 2),
        nullable=True,
    )

    is_available = Column(
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

    branch = relationship(
        "Branch",
        back_populates="inventory_items",
    )

    product_variant = relationship(
        "ProductVariant",
        back_populates="branch_inventory",
    )