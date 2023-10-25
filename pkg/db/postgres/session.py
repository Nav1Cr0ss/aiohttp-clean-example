from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from pkg.db.postgres.connection import engine

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
