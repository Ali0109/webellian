import logging

from app.schemas.product import ProductUpdate, ProductResponse
from app.repositories.product_repository import ProductRepository
from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class UpdateProduct:
    def __init__(
        self, product_repository: ProductRepository, catalog_repository: CatalogRepository
    ) -> None:
        self.product_repository = product_repository
        self.catalog_repository = catalog_repository

    async def execute(
        self,
        product_id: int,
        product_data: ProductUpdate,
    ) -> ProductResponse:
        logger.info(f"Updating product with id: {product_id}")

        product = await self.product_repository.get_by_id(product_id)
        if not product:
            logger.warning(f"Product with id {product_id} not found")
            raise NotFoundError("Product", product_id)

        update_data = product_data.model_dump(exclude_unset=True)

        if "catalog_id" in update_data and update_data["catalog_id"] is not None:
            catalog = await self.catalog_repository.get_by_id(update_data["catalog_id"])
            if not catalog:
                logger.warning(f"Catalog with id {update_data['catalog_id']} not found")
                raise NotFoundError("Catalog", update_data["catalog_id"])

        return await self.product_repository.update(product_id, product_data)
