from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import logging

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product_data: ProductCreate) -> ProductResponse:
        logger.info(
            f"Creating product with name: {product_data.name}, catalog_id: {product_data.catalog_id}"
        )
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            quantity=product_data.quantity,
            catalog_id=product_data.catalog_id,
        )
        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        logger.info(f"Product created with id: {product.id}")
        return ProductResponse.model_validate(product)

    async def get_by_id(self, product_id: int) -> Optional[ProductResponse]:
        logger.debug(f"Fetching product with id: {product_id}")
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return None
        return ProductResponse.model_validate(product)

    async def get_by_catalog_id(
        self,
        catalog_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[ProductResponse], int]:
        logger.debug(
            f"Fetching products for catalog_id: {catalog_id} - page: {page}, page_size: {page_size}"
        )

        count_result = await self.session.execute(
            select(func.count(Product.id)).where(Product.catalog_id == catalog_id)
        )
        total = count_result.scalar() or 0

        offset = (page - 1) * page_size
        result = await self.session.execute(
            select(Product)
            .where(Product.catalog_id == catalog_id)
            .offset(offset)
            .limit(page_size)
            .order_by(Product.created_at.desc())
        )
        products = result.scalars().all()

        logger.debug(
            f"Fetched {len(products)} products out of {total} total for catalog {catalog_id}"
        )
        return [ProductResponse.model_validate(p) for p in products], total

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[ProductResponse], int]:
        logger.debug(f"Fetching all products - page: {page}, page_size: {page_size}")

        count_result = await self.session.execute(select(func.count(Product.id)))
        total = count_result.scalar() or 0

        offset = (page - 1) * page_size
        result = await self.session.execute(
            select(Product).offset(offset).limit(page_size).order_by(Product.created_at.desc())
        )
        products = result.scalars().all()

        logger.debug(f"Fetched {len(products)} products out of {total} total")
        return [ProductResponse.model_validate(p) for p in products], total

    async def update(self, product_id: int, product_data: ProductUpdate) -> ProductResponse:
        logger.info(f"Updating product with id: {product_id}")
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        update_data = product_data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            product.name = update_data["name"]
        if "description" in update_data:
            product.description = update_data["description"]
        if "price" in update_data and update_data["price"] is not None:
            product.price = update_data["price"]
        if "quantity" in update_data and update_data["quantity"] is not None:
            product.quantity = update_data["quantity"]
        if "catalog_id" in update_data:
            product.catalog_id = update_data["catalog_id"]

        await self.session.flush()
        await self.session.refresh(product)
        logger.info(f"Product updated: {product.id}")
        return ProductResponse.model_validate(product)

    async def delete(self, product_id: int) -> None:
        logger.info(f"Deleting product with id: {product_id}")
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        await self.session.delete(product)
        await self.session.flush()
        logger.info(f"Product deleted: {product_id}")
