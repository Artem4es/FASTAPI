import uuid
from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from src.database import Base, get_async_session, metadata

UUID_ID = uuid.UUID


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    metadata = metadata

    if TYPE_CHECKING:  #   pragma: no cover
        username: str
    else:
        username: Mapped[bool] = Column(
            String(length=50), unique=True, default=False, nullable=False
        )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
