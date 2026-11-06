from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Novel Studio"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_novel"
    redis_url: str = "redis://localhost:6379/0"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
