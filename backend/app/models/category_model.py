# app/models/category_model.py

import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from  app.database.database import Base


class Category(Base):
    __tablename__ = "categories"

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
    image_url = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    subcategories = relationship(
        "SubCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )