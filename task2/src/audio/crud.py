from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from audio.models import Audio


async def save_audio(
    filename: str,
    filepath: str,
    user_id: str,
    session: AsyncSession,
) -> str:
    """Save audio ref in db"""
    new_audio = Audio(filename=filename, filepath=filepath, user_id=user_id)
    session.add(new_audio)
    await session.flush()
    await session.commit()
    return new_audio.id


async def get_audio(
    file_uuid: str,
    user_uuid: str,
    session: AsyncSession,
) -> str:
    """Get audio from db"""
    q = select(Audio).filter(Audio.id == file_uuid, Audio.user_id == user_uuid)
    result = await session.execute(q)
    audio = result.scalar()
    return audio
