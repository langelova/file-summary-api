from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the app. Environment variables are automatically loaded from `.env`.
    Defaults are provided for tests to avoid validation errors.
    """

    DB_HOST: str = "somehost"
    DB_PORT: str = "5432"
    DB_NAME: str = "example"
    DB_USER: str = "user"
    DB_PASS: str = "password"
    ENV: str = "test"
    VERSION: str = "0.0.1"
    CHATGPT_API_KEY: str = "example-api-key"

    class Config:
        env_file = ".env"  # Automatically load from .env
        env_file_encoding = "utf-8"


# Instantiate the settings object
settings = Settings()
