from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    SecretStr
)

class Settings(BaseSettings):
    pg_dsn: PostgresDsn = f"postgresql+asyncpg://username:password@localhost:5432/traveling"
    pg_retries = 10
    pg_retry_delay = 1
    pg_echo = False


    redis_host = "localhost"
    redis_port = "6379"


    jwt_secret_key: SecretStr

    model_config = SettingsConfigDict(env_file=".env", str_to_lower=True, env_prefix="APP_")

settings = Settings()

