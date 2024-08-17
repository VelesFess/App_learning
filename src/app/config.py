from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: str = (
        "postgresql+asyncpg://alan:wakeupalan@postgres:5432/alanwake"  # noqa: E501
    )
    auth_secret: str = "AUTH_SECRET"


settings = Settings()
