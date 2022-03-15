from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    READ_SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
