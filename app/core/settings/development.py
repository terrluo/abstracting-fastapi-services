import logging

from app.core.settings.app import AppSettings, SqliteDsn


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Fastapi Service"

    database_url: SqliteDsn

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
