import logging

from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class DeleteCatalog:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    async def execute(self, catalog_id: int) -> None:
        logger.info(f"Deleting catalog with id: {catalog_id}")

        catalog = await self.repository.get_by_id(catalog_id)
        if not catalog:
            logger.warning(f"Catalog with id {catalog_id} not found")
            raise NotFoundError("Catalog", catalog_id)

        await self.repository.delete(catalog_id)
        logger.info(f"Catalog {catalog_id} deleted successfully")
