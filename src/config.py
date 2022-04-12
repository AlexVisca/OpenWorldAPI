from pydantic import BaseSettings


class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_AUTH: str

    class Config:
        env_file = ".env"

settings = Settings()
