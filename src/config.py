from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    DATABASE: str = "sqlite:///./test.sqlite3"
    API_V1_PREFIX: str = "/api/v1"
    DB_ECHO_LOG: bool = True
    PORT: int = 7013
    DEBUG: bool = True
    # DB_POOL_SIZE: int = 5
    # DB_MAX_OVERFLOW: int = 10
    # DB_POOL_TIMEOUT: int = 30
    # DB_POOL_RECYCLE: int = 1800

    class Config:
        env_file = ".env"


settings = Settings()
