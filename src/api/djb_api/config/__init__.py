from os import getenv
from typing import cast

from djb_api.config.db import DBConfig
from djb_api.config.jwt import JWTConfig


class Config:
    db: DBConfig
    jwt: JWTConfig
    ENV: str
    DEBUG: bool
    TESTING: bool
    LOGGING_LEVEL: str
    APP_URL: str
    BLOCK_REGISTER: bool
    PUBLIC_PATH: str
    PRIVATE_PATH: str


class DevConfig(Config):
    from .db import DevConfig as db
    from .jwt import DevConfig as jwt

    ENV = "development"
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = "DEBUG"
    APP_URL = getenv("APP_URL", "localhost")
    BLOCK_REGISTER = bool(getenv("BLOCK_REGISTER", False))
    PUBLIC_PATH = getenv("PUBLIC_PATH", "./media/public/")
    PRIVATE_PATH = getenv("PRIVATE_PATH", "./media/private/")


class ProdConfig:
    from .db import ProdConfig as db
    from .jwt import ProdConfig as jwt

    ENV = "production"
    DEBUG = False
    TESTING = False
    LOGGING_LEVEL = "WARNING"
    APP_URL = getenv("APP_URL", None)
    BLOCK_REGISTER = bool(getenv("BLOCK_REGISTER", False))
    PUBLIC_PATH = getenv("PUBLIC_PATH", "./media/public/")
    PRIVATE_PATH = getenv("PRIVATE_PATH", "./media/private/")


configs = {
    "development": DevConfig,
    "production": ProdConfig,
}

environment = getenv("ENV", "production")
config = cast(Config, configs.get(environment, ProdConfig))
