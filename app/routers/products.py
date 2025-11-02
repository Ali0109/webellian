from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.repositories.catalog_repository import CatalogRepository
from app.services.product import (
    CreateProduct,
    GetProduct,
    GetProductList,
    UpdateProduct,
    DeleteProduct,
)
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse

router = APIRouter()


def get_product_repository(
    session: AsyncSession = Depends(get_db),
) -> ProductRepository:
    return ProductRepository(session)


def get_catalog_repository(
    session: AsyncSession = Depends(get_db),
) -> CatalogRepository:
    return CatalogRepository(session)


@router.post("/products", status_code=201)
async def create_product(
    product_data: ProductCreate,
    product_repository: ProductRepository = Depends(get_product_repository),
    catalog_repository: CatalogRepository = Depends(get_catalog_repository),
) -> ProductResponse:
    service = CreateProduct(product_repository, catalog_repository)
    return await service.execute(product_data)


@router.get("/products")
async def get_products(
    catalog_id: Optional[int] = Query(None, description="Filter by catalog ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    product_repository: ProductRepository = Depends(get_product_repository),
    catalog_repository: CatalogRepository = Depends(get_catalog_repository),
) -> ProductListResponse:
    service = GetProductList(product_repository, catalog_repository)
    return await service.execute(catalog_id=catalog_id, page=page, page_size=page_size)


@router.get("/products/{product_id}")
async def get_product(
    product_id: int,
    product_repository: ProductRepository = Depends(get_product_repository),
) -> ProductResponse:
    service = GetProduct(product_repository)
    return await service.execute(product_id)


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_repository: ProductRepository = Depends(get_product_repository),
    catalog_repository: CatalogRepository = Depends(get_catalog_repository),
) -> ProductResponse:
    service = UpdateProduct(product_repository, catalog_repository)
    return await service.execute(product_id, product_data)


@router.delete("/products/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    product_repository: ProductRepository = Depends(get_product_repository),
) -> None:
    service = DeleteProduct(product_repository)
    await service.execute(product_id)
