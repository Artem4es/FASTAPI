import uuid
from typing import TYPE_CHECKING, AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import MetaData, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, async_session_maker
from src.settings import REAL_DATABASE_URL

DATABASE_URL = REAL_DATABASE_URL
UUID_ID = uuid.UUID


metadata = MetaData()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    metadata = metadata

    if TYPE_CHECKING:  #   pragma: no cover
        username: str
    else:
        username: Mapped[bool] = mapped_column(
            String(length=50), unique=True, default=False, nullable=False
        )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
