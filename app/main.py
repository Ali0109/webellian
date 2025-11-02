from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import logging

from app.config import settings
from app.routers import catalogs, products
from app.models import Catalog, Product  # noqa: F401

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A FastAPI application for managing shop inventory",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalogs.router, prefix=settings.API_V1_PREFIX, tags=["catalogs"])
app.include_router(products.router, prefix=settings.API_V1_PREFIX, tags=["products"])


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "message": "Welcome to Webellian Shop Inventory API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
