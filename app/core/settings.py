from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config import Environment, get_current_environment


ENV_FILES = {
    Environment.DEV: ".env.dev",
    Environment.TEST: ".env.test",
    Environment.PROD: ".env.prod",
}


def get_env_file() -> str:
    return ENV_FILES[get_current_environment()]


class Settings(BaseSettings):
    project_name: str = "Todo API"
    project_version: str = "0.1.0"
    debug: bool = False

    database_url: str

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()