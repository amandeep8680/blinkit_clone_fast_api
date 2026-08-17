from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubCategoryBase(BaseModel):
    name: str
    slug: str
    image_url: Optional[str] = None
    is_active: bool = True


class SubCategoryCreate(SubCategoryBase):
    category_unique_id: str


class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    image_url: Optional[str] = None
    


class SubCategoryResponse(SubCategoryBase):
    unique_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)