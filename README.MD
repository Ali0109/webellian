# Webellian Technical Task

## 🛠️ Task Demonstration:

Developed a Python FastAPI application for managing shop inventory. The application includes the following functionalities:

## 📦 Catalog Management:

- Functionality for retrieving a list of catalogs with pagination.
- Functionality for add, update, or delete catalogs with async database connection and high throughput system performance.

## 🛒 Product Management:

- Retrieve a list of products within a specific catalog.
- Create, update, or delete products.
- Assign or remove a product from a catalog.

## 📑 API Documentation and Testing:

- Provided API documentation using Swagger (OpenAPI), which is built-in with FastAPI.
- Application can be tested effectively via the auto-generated Swagger UI at http://localhost:9000/docs.

## 🗄️ Database:

- Persistent database PostgreSQL with ORM SQLAlchemy (async).
- Database migrations using Alembic.
- Clean architecture with ORM models, repositories, services, and routers.

## ✅ Architecture:

- **Model Layer**: ORM models (SQLAlchemy 2.0) representing Catalog and Product entities.
- **Repository Layer**: Data access layer using async SQLAlchemy. Repositories accept and return Pydantic schemas.
- **Service Layer**: Business logic layer (SRP) that uses repositories.
- **Router Layer**: API endpoints (controllers) that use services with dependency injection.
- **Schema Layer**: Pydantic models for API request/response validation with BaseSchema for common configuration.

## 📂 Features Implemented:

- ✅ Dependency injection using FastAPI Depends.
- ✅ Unit tests with pytest and httpx.
- ✅ Docker and Docker Compose setup.
- ✅ Proper logging throughout the application.
- ✅ Error handling with custom exceptions.
- ✅ Async database operations for high performance.

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.13 (if running locally)

### Running with Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Ali0109/webellian
cd webellian
```

2. Build and start the application:
```bash
docker-compose up --build
```

3. The application will be available at:
   - API: http://localhost:9000
   - Swagger UI: http://localhost:9000/docs
   - ReDoc: http://localhost:9000/redoc

4. To stop the application:
```bash
docker-compose down
```

### Running Locally

1. Install dependencies using `uv`:
```bash
uv pip install -e .
```

2. Make sure PostgreSQL is running and update DATABASE_URL in `.env` file if needed.

3. Run database migrations:
```bash
alembic upgrade head
```

4. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

## 🧪 Running Tests

To run the test suite:

```bash
make test
```

or

```bash
uv run pytest tests/ -v
```

## 📁 Project Structure

```
webellian/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── database.py          # Database connection and session management
│   ├── exceptions.py        # Custom exceptions
│   ├── models/              # ORM models (SQLAlchemy 2.0)
│   │   ├── catalog.py
│   │   └── product.py
│   ├── repositories/        # Data access layer
│   │   ├── catalog_repository.py
│   │   └── product_repository.py
│   ├── services/            # Business logic layer (SRP)
│   │   ├── catalog/
│   │   │   ├── create_catalog.py
│   │   │   ├── get_catalog.py
│   │   │   ├── get_catalog_list.py
│   │   │   ├── update_catalog.py
│   │   │   └── delete_catalog.py
│   │   └── product/
│   │       ├── create_product.py
│   │       ├── get_product.py
│   │       ├── get_product_list.py
│   │       ├── update_product.py
│   │       ├── delete_product.py
│   │       ├── assign_to_catalog.py
│   │       └── remove_from_catalog.py
│   ├── routers/             # API endpoints (controllers)
│   │   ├── catalogs.py
│   │   └── products.py
│   └── schemas/             # Pydantic models for API
│       ├── base.py          # BaseSchema with model_config
│       ├── catalog.py
│       └── product.py
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── versions/
│   └── script.py.mako
├── tests/                   # Unit tests
│   ├── conftest.py
│   ├── test_catalogs.py
│   └── test_products.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml            # Project configuration (uv, ruff)
├── alembic.ini              # Alembic configuration
├── Makefile                 # Development commands
└── README.md
```

## 🔧 Configuration

Environment variables can be set in `.env` file:

- `DATABASE_URL`: PostgreSQL connection string (default: `postgresql+asyncpg://postgres:postgres@db:5432/webellian_db`)
- `DEBUG`: Enable debug mode (default: `False`)

## 🛠️ Development

### Installing Dependencies

The project uses `uv` for package management:

```bash
# Install uv if not already installed
pip install uv

# Install project dependencies
uv pip install -e .
```

### Code Quality

The project uses `ruff` for linting and formatting:

```bash
# Format code
make format
# or
ruff format app tests

# Lint code
make lint
# or
ruff check app tests

# Run all checks
make dev
```

### Running Tests

```bash
# Run tests
make test
# or
uv run pytest tests/ -v
```

## 📝 Architecture Notes

- **Single Responsibility Principle (SRP)**: Each service class has a single responsibility (e.g., `CreateCatalog`, `UpdateCatalog`, etc.).
- **Dependency Injection**: Services are injected into routers via FastAPI's `Depends`. Database transactions are managed by FastAPI's dependency system.
- **Async Operations**: All database operations are async for better performance.
- **Clean Architecture**: The application follows clean architecture principles with clear separation of concerns:
  - Model layer: ORM models (SQLAlchemy 2.0 with Mapped syntax)
  - Repository layer: Data access (accepts and returns Pydantic schemas)
  - Service layer: Business logic (split by SRP)
  - Router layer: API endpoints
- **Logging**: Configured throughout the application for better observability.
- **Code Quality**: The project uses `ruff` for linting and formatting (configured in `pyproject.toml`).
