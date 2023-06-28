import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from audio.crud import get_audio, save_audio
from audio.models import User
from audio.resoponses import no_file, wrong_format
from audio.schemas import RespUrlModel
from auth.manager import current_active_user
from src.database import get_async_session
from src.settings import AUDIO_DIR

router = APIRouter()


@router.get('/record/', responses=no_file)
async def get_record(
    id: uuid.UUID,
    user: uuid.UUID,
    user_obj: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Returns download link"""

    file = await get_audio(id, user, session)
    if not file:
        raise HTTPException(
            status_code=400,
            detail="У нас нет такого файла :(",
        )
    filepath = file.filepath
    filename = file.filename
    return FileResponse(
        path=filepath, filename=filename, media_type='audio/mpeg'
    )


@router.post("/uploadfile/", responses=wrong_format)
async def create_upload_file(
    file: UploadFile,
    request: Request,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> RespUrlModel:
    try:
        wav_path = os.path.join(AUDIO_DIR, "wav", file.filename)
        with open(
            wav_path, "wb"
        ) as f:  # в данном случае возможно лучше использовать синхронную функ
            # может использовть aiofiles
            f.write(await file.read())
            f.close()
        sound = AudioSegment.from_wav(wav_path)
        new_filename = f'{uuid.uuid4()}.mp3'
        new_path = os.path.join(AUDIO_DIR, "mp3", new_filename)
        sound.export(new_path, format="mp3")  # правда тут будет тормоз

        audio_id = await save_audio(
            filename=new_filename,
            filepath=new_path,
            user_id=user.id,
            session=session,
        )
    except (CouldntDecodeError, IndexError):  # IndexError for .jpg
        raise HTTPException(
            status_code=400,
            detail="Убедитесь, что загружаете файл в формате .wav",
        )

    base_url = str(request.base_url)  # Получаем базовый URL сервера
    download_url = f"{base_url}record?id={audio_id}&user={user.id}"
    return RespUrlModel(download_link=download_url)
