from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import logging



class AppConfig(BaseSettings):
    app_name: str
    app_env: str
    database_url: str
    log_level: int = logging.DEBUG
    allowed_origins: list[str] = ["http://localhost:3001"]


    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def getAppConfig():
    return AppConfig()  # type: ignore
