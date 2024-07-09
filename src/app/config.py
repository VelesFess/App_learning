from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: PostgresDsn = (
        "postgresql+asyncpg://alan:wakeupalan@localhost:5432/wake"  # noqa: E501
    )


settings = Settings()
