from sqlalchemy import select

from audio.models import Audio
from src.database import async_session_maker


async def save_audio(filename: str, filepath: str, user_id: str) -> str:
    """Save audio ref in db"""
    # async with async_session() as session:
    async with async_session_maker() as session:
        async with session.begin():
            new_audio = Audio(
                filename=filename, filepath=filepath, user_id=user_id
            )
            session.add(new_audio)
            await session.flush()
            return new_audio.id


async def get_audio(file_uuid: str, user_uuid: str) -> str:
    """Save audio ref in db"""
    async with async_session_maker() as session:
        async with session.begin():
            q = select(Audio).filter(
                Audio.id == file_uuid, Audio.user_id == user_uuid
            )
            result = await session.execute(q)
            audio = result.scalar()
            return audio
