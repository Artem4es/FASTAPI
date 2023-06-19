import os
import uuid

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from fastapi_responses import custom_openapi
from fastapi_users import FastAPIUsers
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from audio.models import Audio
from audio.schemas import RespUrlModel
from auth.base_config import auth_backend
from auth.manager import current_active_user, get_user_manager
from auth.models import User
from auth.schemas import UserCreate, UserRead
from database import async_session
from settings import AUDIO_DIR, REAL_DATABASE_URL

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################


# create async engine for interaction with database
# engine = create_async_engine(REAL_DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )


###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


async def save_audio(filename: str, filepath: str, user_id: str) -> str:
    """Save audio ref in db"""
    async with async_session() as session:
        async with session.begin():
            new_audio = Audio(
                filename=filename, filepath=filepath, user_id=user_id
            )
            session.add(new_audio)
            await session.flush()
            return new_audio.id


async def get_audio(file_uuid: str, user_uuid: str) -> str:
    """Save audio ref in db"""
    async with async_session() as session:
        async with session.begin():
            q = select(Audio).filter(
                Audio.id == file_uuid, Audio.user_id == user_uuid
            )
            result = await session.execute(q)
            audio = result.scalar()
            return audio


#########################
# BLOCK WITH API ROUTES #
#########################


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


app = FastAPI()

app.openapi = custom_openapi(app)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


router = APIRouter()


@router.get('/record/')
async def get_record(
    id: uuid.UUID,
    user: uuid.UUID,
    user_obj: User = Depends(current_active_user),
):
    """Returns download link"""
    file = await get_audio(id, user)
    filepath = file.filepath
    filename = file.filename
    return FileResponse(
        path=filepath, filename=filename, media_type='audio/mpeg'
    )


# class RespUrlModel(BaseModel):
#     download_link: str


@router.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile,
    request: Request,
    user: User = Depends(current_active_user),
) -> RespUrlModel:
    try:
        wav_path = os.path.join(AUDIO_DIR, "wav", file.filename)
        with open(wav_path, "wb") as f:
            f.write(await file.read())
            f.close()
        sound = AudioSegment.from_wav(wav_path)
        base_name = os.path.splitext(file.filename)[0]
        new_filename = f'{base_name}.mp3'
        new_path = os.path.join(AUDIO_DIR, "mp3", new_filename)
        sound.export(new_path, format="mp3")

        audio_id = await save_audio(
            filename=new_filename, filepath=new_path, user_id=user.id
        )
    except CouldntDecodeError:
        raise HTTPException(
            400, 'Убедитесь, что загружаете файл с расширением wav'
        )

    base_url = str(request.base_url)  # Получаем базовый URL сервера
    download_url = f"{base_url}record?id={audio_id}&user={user.id}"
    return RespUrlModel(download_link=download_url)


app.include_router(router, prefix='', tags=["audio"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)