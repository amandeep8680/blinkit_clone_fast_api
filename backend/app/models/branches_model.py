import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from  app.database.database import Base


class Branch(Base):
    """Represents a Blinkit branch/store location."""

    __tablename__ = "branches"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    unique_id = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    name = Column(
        String(150),
        nullable=False,
    )

    address = Column(
        String(500),
        nullable=False,
    )

    city = Column(
        String(100),
        nullable=False,
    )

    pincode = Column(
        String(10),
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
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # One-to-one relationship with BranchManager.
    manager = relationship(
        "BranchManager",
        back_populates="branch",
        uselist=False,
    )


    inventory_items = relationship(
    "BranchInventory",
    back_populates="branch",
    cascade="all, delete-orphan",
)

    carts = relationship(
    "Cart",
    back_populates="branch",
)