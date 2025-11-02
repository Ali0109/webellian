from typing import Optional
import logging

from app.schemas.product import ProductListResponse
from app.repositories.product_repository import ProductRepository
from app.repositories.catalog_repository import CatalogRepository
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class GetProductList:
    def __init__(
        self, product_repository: ProductRepository, catalog_repository: CatalogRepository
    ) -> None:
        self.product_repository = product_repository
        self.catalog_repository = catalog_repository

    async def execute(
        self,
        catalog_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> ProductListResponse:
        logger.debug(
            f"Getting products - catalog_id: {catalog_id}, page: {page}, page_size: {page_size}"
        )

        if catalog_id:
            catalog = await self.catalog_repository.get_by_id(catalog_id)
            if not catalog:
                logger.warning(f"Catalog with id {catalog_id} not found")
                raise NotFoundError("Catalog", catalog_id)

            products, total = await self.product_repository.get_by_catalog_id(
                catalog_id=catalog_id,
                page=page,
                page_size=page_size,
            )
        else:
            products, total = await self.product_repository.get_all(
                page=page,
                page_size=page_size,
            )

        return ProductListResponse(
            items=products,
            total=total,
            page=page,
            page_size=page_size,
        )
