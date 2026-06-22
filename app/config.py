import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    db_url = os.getenv("DATABASE_URL")

    if db_url:
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        user = os.getenv("POSTGRES_USER")
        password = quote_plus(os.getenv("POSTGRES_PASSWORD", ""))
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB")

        if all([user, password, host, db_name]):
            SQLALCHEMY_DATABASE_URI = (f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
        else:
            raise RuntimeError("Configuração do banco não encontrada")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")