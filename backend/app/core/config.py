from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"

    secret_key: str = "change_this_to_a_long_random_secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/tasks_db"
    frontend_origin: str = "http://localhost:5173"

    external_api_url: str = "https://httpbin.org/status/200"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
