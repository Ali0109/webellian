from pydantic import Field
from datetime import datetime
from typing import List, Optional

from app.schemas.base import BaseSchema


class ProductBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    quantity: int = Field(0, ge=0, description="Product quantity")


class ProductCreate(ProductBase):
    catalog_id: Optional[int] = Field(None, description="Catalog ID to assign product to")


class ProductUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[float] = Field(None, gt=0, description="Product price")
    quantity: Optional[int] = Field(None, ge=0, description="Product quantity")
    catalog_id: Optional[int] = Field(None, description="Catalog ID to assign product to")


class ProductResponse(ProductBase):
    id: int
    catalog_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseSchema):
    items: List[ProductResponse]
    total: int
    page: int = 1
    page_size: int = 10
