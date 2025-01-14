from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = dict(env_file=".env")

    # SQLALCHEMY_DATABASE_URI: str = "postgresql+asyncpg://user:password@localhost/dbname"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test.sqlite3"
    API_V1_PREFIX: str = "/api/v1"
    DB_ECHO_LOG: bool = True
    PORT: int = 7012
    DEBUG: bool = True
    TESTING: bool = False
    # DB_POOL_SIZE: int = 5
    # DB_MAX_OVERFLOW: int = 10
    # DB_POOL_TIMEOUT: int = 30
    # DB_POOL_RECYCLE: int = 1800


settings = Settings()
