from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import logging

from app.models.catalog import Catalog
from app.schemas.catalog import CatalogCreate, CatalogUpdate, CatalogResponse

logger = logging.getLogger(__name__)


class CatalogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, catalog_data: CatalogCreate) -> CatalogResponse:
        logger.info(f"Creating catalog with name: {catalog_data.name}")
        catalog = Catalog(name=catalog_data.name, description=catalog_data.description)
        self.session.add(catalog)
        await self.session.flush()
        await self.session.refresh(catalog)
        logger.info(f"Catalog created with id: {catalog.id}")
        return CatalogResponse.model_validate(catalog)

    async def get_by_id(self, catalog_id: int) -> Optional[CatalogResponse]:
        logger.debug(f"Fetching catalog with id: {catalog_id}")
        result = await self.session.execute(select(Catalog).where(Catalog.id == catalog_id))
        catalog = result.scalar_one_or_none()
        if not catalog:
            return None
        return CatalogResponse.model_validate(catalog)

    async def get_by_name(self, name: str) -> Optional[CatalogResponse]:
        logger.debug(f"Fetching catalog with name: {name}")
        result = await self.session.execute(select(Catalog).where(Catalog.name == name))
        catalog = result.scalar_one_or_none()
        if not catalog:
            return None
        return CatalogResponse.model_validate(catalog)

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> tuple[List[CatalogResponse], int]:
        logger.debug(f"Fetching catalogs - page: {page}, page_size: {page_size}")

        count_result = await self.session.execute(select(func.count(Catalog.id)))
        total = count_result.scalar() or 0

        offset = skip if skip is not None else (page - 1) * page_size
        limit_val = limit if limit is not None else page_size

        result = await self.session.execute(
            select(Catalog).offset(offset).limit(limit_val).order_by(Catalog.created_at.desc())
        )
        catalogs = result.scalars().all()

        logger.debug(f"Fetched {len(catalogs)} catalogs out of {total} total")
        return [CatalogResponse.model_validate(c) for c in catalogs], total

    async def update(self, catalog_id: int, catalog_data: CatalogUpdate) -> CatalogResponse:
        logger.info(f"Updating catalog with id: {catalog_id}")
        result = await self.session.execute(select(Catalog).where(Catalog.id == catalog_id))
        catalog = result.scalar_one_or_none()
        if not catalog:
            raise ValueError(f"Catalog with id {catalog_id} not found")

        if catalog_data.name is not None:
            catalog.name = catalog_data.name
        if catalog_data.description is not None:
            catalog.description = catalog_data.description

        await self.session.flush()
        await self.session.refresh(catalog)
        logger.info(f"Catalog updated: {catalog.id}")
        return CatalogResponse.model_validate(catalog)

    async def delete(self, catalog_id: int) -> None:
        logger.info(f"Deleting catalog with id: {catalog_id}")
        result = await self.session.execute(select(Catalog).where(Catalog.id == catalog_id))
        catalog = result.scalar_one_or_none()
        if not catalog:
            raise ValueError(f"Catalog with id {catalog_id} not found")
        await self.session.delete(catalog)
        await self.session.flush()
        logger.info(f"Catalog deleted: {catalog_id}")
