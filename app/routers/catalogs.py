from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.repositories.catalog_repository import CatalogRepository
from app.services.catalog import (
    CreateCatalog,
    GetCatalog,
    GetCatalogList,
    UpdateCatalog,
    DeleteCatalog,
)
from app.schemas.catalog import CatalogCreate, CatalogUpdate, CatalogResponse, CatalogListResponse

router = APIRouter()


def get_catalog_repository(
    session: AsyncSession = Depends(get_db),
) -> CatalogRepository:
    return CatalogRepository(session)


@router.post("/catalogs", status_code=201)
async def create_catalog(
    catalog_data: CatalogCreate,
    repository: CatalogRepository = Depends(get_catalog_repository),
) -> CatalogResponse:
    service = CreateCatalog(repository)
    return await service.execute(catalog_data)


@router.get("/catalogs")
async def get_catalogs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    skip: Optional[int] = Query(None, ge=0, description="Skip records"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit records"),
    repository: CatalogRepository = Depends(get_catalog_repository),
) -> CatalogListResponse:
    service = GetCatalogList(repository)
    return await service.execute(page=page, page_size=page_size, skip=skip, limit=limit)


@router.get("/catalogs/{catalog_id}")
async def get_catalog(
    catalog_id: int,
    repository: CatalogRepository = Depends(get_catalog_repository),
) -> CatalogResponse:
    service = GetCatalog(repository)
    return await service.execute(catalog_id)


@router.put("/catalogs/{catalog_id}")
async def update_catalog(
    catalog_id: int,
    catalog_data: CatalogUpdate,
    repository: CatalogRepository = Depends(get_catalog_repository),
) -> CatalogResponse:
    service = UpdateCatalog(repository)
    return await service.execute(catalog_id, catalog_data)


@router.delete("/catalogs/{catalog_id}", status_code=204)
async def delete_catalog(
    catalog_id: int,
    repository: CatalogRepository = Depends(get_catalog_repository),
) -> None:
    service = DeleteCatalog(repository)
    await service.execute(catalog_id)
