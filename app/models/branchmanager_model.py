import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.constants.roles import BRANCH_MANAGER


class BranchManager(Base):
    """Represents a manager assigned to a branch."""

    __tablename__ = "branch_managers"

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
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(50),
        nullable=False,
        default=BRANCH_MANAGER,
    )

    # Internal database relationship.
    # nullable=True allows creating a manager before assigning a branch.
    branch_id = Column(
        Integer,
        ForeignKey("branches.id"),
        nullable=True,
        unique=True,
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

    # Gives access to the assigned Branch object.
    branch = relationship(
        "Branch",
        back_populates="manager",
    )