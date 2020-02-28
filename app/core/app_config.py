from enum import Enum
from os import getenv
from typing import Dict


class Environment(Enum):
    LOCALHOST = "LOCALHOST"
    PRODUCTION = "PRODUCTION"


class AppConfig:

    _environment: Environment = Environment(getenv("ENVIRONMENT", "LOCALHOST"))

    @staticmethod
    def is_production() -> bool:
        return AppConfig._environment == Environment.PRODUCTION

    @staticmethod
    def is_localhost() -> bool:
        return AppConfig._environment == Environment.LOCALHOST

    @staticmethod
    def cors() -> Dict[str, str]:
        return {"origins": "http://localhost:3000" if AppConfig.is_localhost() else "https://venues.n-kj.nl"}

    @staticmethod
    def get_port() -> int:
        return int(getenv("PORT", "8080"))
