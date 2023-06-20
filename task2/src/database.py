from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

import src.settings as settings

Base = declarative_base()

# create async engine for interaction with database
engine = create_async_engine(
    settings.REAL_DATABASE_URL, future=True, echo=True
)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
