# app/models/brand_model.py

import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, DateTime , Integer
from sqlalchemy.sql import func

from  app.database.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    name = Column(String, unique=True, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    logo_url = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


    products = relationship(
    "Product",
    back_populates="brand",
)