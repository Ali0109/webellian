from pydantic import Field
from datetime import datetime
from typing import List, Optional

from app.schemas.base import BaseSchema


class CatalogBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255, description="Catalog name")
    description: Optional[str] = Field(None, description="Catalog description")


class CatalogCreate(CatalogBase):
    pass


class CatalogUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Catalog name")
    description: Optional[str] = Field(None, description="Catalog description")


class CatalogResponse(CatalogBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CatalogListResponse(BaseSchema):
    items: List[CatalogResponse]
    total: int
    page: int = 1
    page_size: int = 10
