import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth.models import Base

# import settings


# # create async engine for interaction with database
# engine = create_async_engine(
#     settings.REAL_DATABASE_URL, future=True, echo=True
# )

# # create session for the interaction with database
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )


class Audio(Base):
    __tablename__ = "audiofile"
    id: UUID = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
    )
    filename: str = Column(String, nullable=False, default=None)
    filepath: str = Column(String, nullable=False, default=None)
    user_id: str = Column(UUID(as_uuid=True), ForeignKey("user.id"))
