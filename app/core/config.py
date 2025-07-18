from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str  # Store a hashed password!
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
