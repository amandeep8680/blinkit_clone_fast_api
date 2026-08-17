import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

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

    name = Column(
        String,
        nullable=False,
        index=True,
    )

    slug = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    # Product belongs to one Brand
    brand_id = Column(
        Integer,
        ForeignKey("brands.id"),
        nullable=False,
        index=True,
    )

    # Product belongs to one SubCategory.
    # Category can be accessed through:
    # product.subcategory.category
    subcategory_id = Column(
        Integer,
        ForeignKey("subcategories.id"),
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

    # -------------------------
    # Relationships
    # -------------------------

    brand = relationship(
        "Brand",
        back_populates="products",
    )

    subcategory = relationship(
        "SubCategory",
        back_populates="products",
    )

    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
    )