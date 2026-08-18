# app/schemas/brand_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    logo_url: Optional[str] = None
 


class BrandResponse(BrandBase):
    unique_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)