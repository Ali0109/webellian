import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_catalog(client: AsyncClient):
    response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Catalog"
    assert data["description"] == "Test Description"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_catalogs(client: AsyncClient):
    await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )

    # Get catalogs
    response = await client.get("/api/v1/catalogs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_get_catalog_by_id(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )
    catalog_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/catalogs/{catalog_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == catalog_id
    assert data["name"] == "Test Catalog"


@pytest.mark.asyncio
async def test_update_catalog(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )
    catalog_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/catalogs/{catalog_id}",
        json={"name": "Updated Catalog", "description": "Updated Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Catalog"
    assert data["description"] == "Updated Description"


@pytest.mark.asyncio
async def test_delete_catalog(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )
    catalog_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/catalogs/{catalog_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/api/v1/catalogs/{catalog_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_catalog(client: AsyncClient):
    response = await client.get("/api/v1/catalogs/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate_catalog(client: AsyncClient):
    await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Test Description"}
    )

    response = await client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog", "description": "Another Description"}
    )
    assert response.status_code == 409
