import logging

from app.schemas.catalog import CatalogResponse
from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class GetCatalog:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    async def execute(self, catalog_id: int) -> CatalogResponse:
        logger.debug(f"Getting catalog with id: {catalog_id}")
        catalog = await self.repository.get_by_id(catalog_id)
        if not catalog:
            logger.warning(f"Catalog with id {catalog_id} not found")
            raise NotFoundError("Catalog", catalog_id)
        return catalog
