import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    response = await client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "quantity": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99
    assert data["quantity"] == 10
    assert "id" in data


@pytest.mark.asyncio
async def test_create_product_with_catalog(client: AsyncClient):
    catalog_response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )
    catalog_id = catalog_response.json()["id"]

    response = await client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "quantity": 10,
            "catalog_id": catalog_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["catalog_id"] == catalog_id


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient):
    await client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "quantity": 10,
        },
    )

    response = await client.get("/api/v1/products?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_get_products_by_catalog(client: AsyncClient):
    catalog_response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )
    catalog_id = catalog_response.json()["id"]

    await client.post(
        "/api/v1/products",
        json={"name": "Product 1", "price": 10.0, "quantity": 5, "catalog_id": catalog_id},
    )
    await client.post(
        "/api/v1/products",
        json={"name": "Product 2", "price": 20.0, "quantity": 3, "catalog_id": catalog_id},
    )

    response = await client.get(f"/api/v1/products?catalog_id={catalog_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert all(item["catalog_id"] == catalog_id for item in data["items"])


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "quantity": 10,
        },
    )
    product_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product"


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "quantity": 10,
        },
    )
    product_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/products/{product_id}",
        json={"name": "Updated Product", "price": 149.99, "quantity": 20},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 149.99
    assert data["quantity"] == 20


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "quantity": 10,
        },
    )
    product_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_product(client: AsyncClient):
    response = await client.get("/api/v1/products/99999")
    assert response.status_code == 404
