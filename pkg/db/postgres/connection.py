from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from settings import config

engine = create_async_engine(config.DB.get_conn_string(), echo=config.DEBUG)
