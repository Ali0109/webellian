from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)
    catalog_id: Mapped[int | None] = mapped_column(
        ForeignKey("catalogs.id", ondelete="CASCADE"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    catalog: Mapped["Catalog | None"] = relationship("Catalog", back_populates="products")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', catalog_id={self.catalog_id})>"
