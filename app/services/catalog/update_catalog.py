import logging

from app.schemas.catalog import CatalogUpdate, CatalogResponse
from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import NotFoundError, ConflictError

logger = logging.getLogger(__name__)


class UpdateCatalog:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        catalog_id: int,
        catalog_data: CatalogUpdate,
    ) -> CatalogResponse:
        logger.info(f"Updating catalog with id: {catalog_id}")

        catalog = await self.repository.get_by_id(catalog_id)
        if not catalog:
            logger.warning(f"Catalog with id {catalog_id} not found")
            raise NotFoundError("Catalog", catalog_id)

        if catalog_data.name and catalog_data.name != catalog.name:
            existing = await self.repository.get_by_name(catalog_data.name)
            if existing:
                logger.warning(f"Catalog with name '{catalog_data.name}' already exists")
                raise ConflictError(f"Catalog with name '{catalog_data.name}' already exists")

        return await self.repository.update(catalog_id, catalog_data)
