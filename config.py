import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "railway-reservation-secret")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "railway_system")
    SQLITE_DB_PATH = BASE_DIR / "railway.db"
    USE_MYSQL = os.getenv("USE_MYSQL", "false").lower() == "true"

    @staticmethod
    def get_database_url():
        if Config.USE_MYSQL:
            return (
                f"mysql+mysqlconnector://{Config.DB_USER}:{Config.DB_PASSWORD}"
                f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
            )
        return f"sqlite:///{Config.SQLITE_DB_PATH}"
