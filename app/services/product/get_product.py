import logging

from app.schemas.product import ProductResponse
from app.repositories.product_repository import ProductRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class GetProduct:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    async def execute(self, product_id: int) -> ProductResponse:
        logger.debug(f"Getting product with id: {product_id}")
        product = await self.repository.get_by_id(product_id)
        if not product:
            logger.warning(f"Product with id {product_id} not found")
            raise NotFoundError("Product", product_id)
        return product
