import os
from dotenv import load_dotenv

load_dotenv(".env")


def env_bool(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def database_url():
    explicit_url = os.getenv("DATABASE_URL")

    if explicit_url:
        return explicit_url

    user = os.getenv("DB_USER", "sam")
    password = os.getenv("DB_PASSWORD", "1234")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "samsara_db")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mudar-chave")

    SQLALCHEMY_DATABASE_URI = database_url()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_ENABLED = env_bool("SCHEDULER_ENABLED")
    SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "America/Sao_Paulo")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
