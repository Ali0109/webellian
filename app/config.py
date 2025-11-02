from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/webellian_db"

    APP_NAME: str = "Webellian Shop Inventory"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    API_V1_PREFIX: str = "/api/v1"


settings = Settings()
