import logging

from app.schemas.catalog import CatalogCreate, CatalogResponse
from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import ConflictError

logger = logging.getLogger(__name__)


class CreateCatalog:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    async def execute(self, catalog_data: CatalogCreate) -> CatalogResponse:
        logger.info(f"Creating catalog: {catalog_data.name}")

        existing = await self.repository.get_by_name(catalog_data.name)
        if existing:
            logger.warning(f"Catalog with name '{catalog_data.name}' already exists")
            raise ConflictError(f"Catalog with name '{catalog_data.name}' already exists")

        return await self.repository.create(catalog_data)
