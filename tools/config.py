from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: str
    DATABASE_NAME: str
    TEST_DATABASE_PORT: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5

    class Config:
        env_file = ".env"


setting = Settings()
