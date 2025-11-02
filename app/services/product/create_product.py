import logging

from app.schemas.product import ProductCreate, ProductResponse
from app.repositories.product_repository import ProductRepository
from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class CreateProduct:
    def __init__(
        self, product_repository: ProductRepository, catalog_repository: CatalogRepository
    ) -> None:
        self.product_repository = product_repository
        self.catalog_repository = catalog_repository

    async def execute(self, product_data: ProductCreate) -> ProductResponse:
        logger.info(f"Creating product: {product_data.name}")

        if product_data.catalog_id:
            catalog = await self.catalog_repository.get_by_id(product_data.catalog_id)
            if not catalog:
                logger.warning(f"Catalog with id {product_data.catalog_id} not found")
                raise NotFoundError("Catalog", product_data.catalog_id)

        return await self.product_repository.create(product_data)
