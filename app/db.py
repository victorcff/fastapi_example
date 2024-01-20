from functools import lru_cache
import psycopg
from psycopg_pool import AsyncConnectionPool, ConnectionPool
from app.config import get_settings


settings = get_settings()

connectionInfo = f"user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port} dbname={settings.db_name}"

def get_connection():
  return psycopg.connect(conninfo=connectionInfo)

@lru_cache()
def get_pool():
  return ConnectionPool(conninfo=connectionInfo)

@lru_cache()
def get_async_pool():
  return AsyncConnectionPool(conninfo=connectionInfo)