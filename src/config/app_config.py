import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    app_name: str
    app_env: str
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str
    log_level: int = logging.DEBUG
    allowed_origins: list[str] = ["http://localhost:3001"]
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]
    rate_limit_default: str = "100/minute"


    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def getAppConfig():
    return AppConfig()  # type: ignore
