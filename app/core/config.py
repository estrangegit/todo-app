import os
from enum import StrEnum


class Environment(StrEnum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


def get_current_environment() -> Environment:
    return Environment(os.getenv("APP_ENV", Environment.DEV.value))
