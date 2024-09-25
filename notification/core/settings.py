from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()

env_path = None if bool(getenv("is_prod", default=False)) else "dev.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

    is_prod: str

    donwload_svc: str

    RABBIT_URL: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    audio_queue: str

    sender_email: str
    smtp_server: str
    email_port: int
    login: str
    email_password: str


settings = Settings()
