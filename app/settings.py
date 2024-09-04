""" Application Settings Module
"""
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv(override=True)

def get_env_variable(var_name):
    value = os.environ.get(var_name)
    if value is None:
        logger.error(f"Environment variable {var_name} is not set")
        raise ValueError(f"Set the {var_name} environment variable")
    return value

def get_connection_string(asyncMode: bool = False) -> str:
    engine = get_env_variable("ASYNC_DB_ENGINE" if asyncMode else "DB_ENGINE")
    dbhost = get_env_variable("DB_HOST")
    username = get_env_variable("DB_USERNAME")
    password = get_env_variable("DB_PASSWORD")
    dbname = get_env_variable("DB_NAME")
    connection_string = f"{engine}://{username}:{password}@{dbhost}/{dbname}"
    logger.debug(f"Connection string ({'async' if asyncMode else 'sync'}): {connection_string}")
    return connection_string

# Database Setting
SQLALCHEMY_DATABASE_URL = get_connection_string()
SQLALCHEMY_DATABASE_URL_ASYNC = get_connection_string(asyncMode=True)

# JWT Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

#Password
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
USER_PASSWORD = os.environ.get("USER_PASSWORD")
