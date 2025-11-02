import logging

from app.repositories.product_repository import ProductRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class DeleteProduct:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    async def execute(self, product_id: int) -> None:
        logger.info(f"Deleting product with id: {product_id}")

        product = await self.repository.get_by_id(product_id)
        if not product:
            logger.warning(f"Product with id {product_id} not found")
            raise NotFoundError("Product", product_id)

        await self.repository.delete(product_id)
        logger.info(f"Product {product_id} deleted successfully")
