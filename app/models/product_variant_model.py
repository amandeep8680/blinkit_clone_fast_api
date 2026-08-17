import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    unique_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # SKU should uniquely identify
    # the sellable variant.
    sku = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # Example:
    # value = 500
    # unit = ml
    value = Column(
        String,
        nullable=False,
    )

    unit = Column(
        String,
        nullable=False,
    )

    # Maximum Retail Price
    mrp = Column(
        Numeric(10, 2),
        nullable=False,
    )

    # Actual selling price
    selling_price = Column(
        Numeric(10, 2),
        nullable=False,
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

    product = relationship(
        "Product",
        back_populates="variants",
    )