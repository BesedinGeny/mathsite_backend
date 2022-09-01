import os
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator, EmailStr, AnyHttpUrl


class Settings(BaseSettings):
    # Service Info
    PROJECT_VERSION: str = "2.0.1"
    PROJECT_NAME: str = "mathbesedina - сайт Бесединой О.С."

    # API
    API_V1_STR: str = "/api/v1"

    #HOST: str = "0.0.0.0"
    HOST: str = "localhost"
    PORT: int = os.getenv("PORT", 8000)

    # Corses
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # PostgreSQL Configuration
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mathsite")
    POSTGRES_USER: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    WEB_CONCURRENCY: int = int(os.getenv("WEB_CONCURRENCY", "1"))
    POOL_SIZE: int = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    # Superuser
    FIRST_SUPERUSER: EmailStr = "admin@math.ru"
    FIRST_SUPERUSER_PASSWORD: str = "123123"

    # https://indominusbyte.github.io/fastapi-jwt-auth/configuration/cookies/

    geo_data_by_ip = "https://geolocation-db.com/json/{ip}&position=true"
    CREDENTIALS_FILE: str = os.getenv('CREDENTIALS_FILE', '../app/config/skins-326215-94ed820652d8.json')
    SPREADSHEET_SERVICE_MAIL = 'skins.data@gmail.com'
    MAX_COLUMNS_SPREADSHEET = 50

    # Minio
    # MINIO_ADDR = os.getenv("MINIO_ADDR", "65.21.105.105:9000")
    MINIO_ADDR = os.getenv("MINIO_ADDR", "0.0.0.0:9000")
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minio")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minio123")

    IMAGE_BUCKET_NAME = 'images'
    DUMPS_BUCKET_NAME = 'dumps'

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")

    # Sentry
    ON_PRODUCTION: bool = os.getenv('ON_PRODUCTION', True)  # Выставить на локальных машинах False
    SENTRY_KEY = os.getenv('SENTRY_KEY', "https://16b191a5b9754e308daaf8978d73714c@o1059794.ingest.sentry.io/6048694")
    SENTRY_RELEASE_VERSION: Optional[str] = None

    @validator("SENTRY_RELEASE_VERSION", pre=True)
    def make_release_string(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        version = "@"

        if not values.get("ON_PRODUCTION"):
            version += "test_"
        version += values.get("PROJECT_VERSION")

        return "skins" + version

    OAUTH_SECRET_KEY = os.getenv('OAUTH_SECRET_KEY', "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")  # unused but necessary


settings = Settings()


class CookiesSettings(BaseSettings):
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    authjwt_algorithm: str = "HS256"

    authjwt_secret_key: str = "secret"  # secrets.token_urlsafe(32)

    auth_access_token_lifetime: int = 60 * 60
    auth_refresh_token_lifetime: int = 15 * 60 * 60 * 24

    access_expires: int = timedelta(minutes=60).total_seconds()
    refresh_expires: int = timedelta(days=15).total_seconds()

    authjwt_access_token_expires: int = timedelta(minutes=60).total_seconds()
    authjwt_refresh_token_expires: int = timedelta(days=15).total_seconds()

    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = True
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False

    # Change to "lax" in production to make your website more secure from CSRF Attacks, default is None
    authjwt_cookie_samesite: str = 'lax'


cookies_settings = CookiesSettings()


class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "MATHSITE"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },

    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "SKINS": {"handlers": ["default"], "level": LOG_LEVEL},
    }


log_config = LogConfig().dict()
