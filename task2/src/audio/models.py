import uuid

from sqlalchemy import UUID, Column, ForeignKey, MetaData, String

from auth.models import User
from src.database import Base

metadata = MetaData()


class Audio(Base):
    __tablename__ = "audiofile"
    metadata = metadata
    id: UUID = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
    )
    filename: str = Column(String, nullable=False, default=None)
    filepath: str = Column(String, nullable=False, default=None)
    user_id: str = Column(UUID(as_uuid=True), ForeignKey(User.id))
