from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    SecretStr
)

class Settings(BaseSettings):
    pg_dsn: str = "sqlite+aiosqlite:///database.db"
    pg_retries: int = 10
    pg_retry_delay: int = 1
    pg_echo: bool = False


    redis_host: str = "localhost"
    redis_port: int = "6379"


    jwt_secret_key: SecretStr

    model_config = SettingsConfigDict(env_file=".env", str_to_lower=True, env_prefix="APP_")

settings = Settings()

