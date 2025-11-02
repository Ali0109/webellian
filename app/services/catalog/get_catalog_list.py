from typing import Optional
import logging

from app.schemas.catalog import CatalogListResponse
from app.repositories.catalog_repository import CatalogRepository

logger = logging.getLogger(__name__)


class GetCatalogList:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        page: int = 1,
        page_size: int = 10,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> CatalogListResponse:
        logger.debug(f"Getting catalogs - page: {page}, page_size: {page_size}")
        catalogs, total = await self.repository.get_all(
            page=page,
            page_size=page_size,
            skip=skip,
            limit=limit,
        )

        return CatalogListResponse(
            items=catalogs,
            total=total,
            page=page,
            page_size=page_size,
        )
