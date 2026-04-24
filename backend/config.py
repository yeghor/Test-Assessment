from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, SecretStr


class Settings(BaseSettings):
    sqlite_url: str = "sqlite+aiosqlite:///database.db"
    sqlite_retries: int = 10
    sqlite_retry_delay: int = 1
    sqlite_echo: bool = False

    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%f%z"


settings = Settings()

import aiosqlite

print(aiosqlite.__version__)