# app/schemas/category_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.schemas.subcategory_schema import SubCategoryResponse


class CategoryBase(BaseModel):
    name: str
    slug: str
    image_url: Optional[str] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    unique_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryWithSubCategoriesResponse(CategoryResponse):
    subcategories: List[SubCategoryResponse] = []

    model_config = ConfigDict(from_attributes=True)