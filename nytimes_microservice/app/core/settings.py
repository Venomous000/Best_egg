import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    nyt_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
