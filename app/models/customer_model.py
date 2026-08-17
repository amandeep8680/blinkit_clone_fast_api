# app/models/customer_model.py

import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Customer(Base):
    __tablename__ = "customers"

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

    name = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    phone = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
        default="customer",
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

    # One Customer -> Many Addresses
    addresses = relationship(
        "CustomerAddress",
        back_populates="customer",
        cascade="all, delete-orphan",
    )


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "label",
            name="uq_customer_address_label",
        ),
    )

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
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Example: Home, Work, Office
    label = Column(
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

    is_default = Column(
        Boolean,
        default=False,
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

    customer = relationship(
        "Customer",
        back_populates="addresses",
    )