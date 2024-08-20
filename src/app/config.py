import os

from pydantic_settings import BaseSettings

os.environ["PGDATA"] = "/var/lib/postgresql"


class Settings(BaseSettings):
    pg_dsn: str = "postgresql+asyncpg://alan:wakeupalan@127.0.0.1:5432/wake2"
    auth_secret: str = "AUTH_SECRET"


settings = Settings()
