from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Swibit Lab"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/swibit"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()