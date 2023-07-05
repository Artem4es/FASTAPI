import asyncio
import os
import shutil
import tempfile
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from audio.dependencies import get_mp3_folder, get_wav_folder
from src.database import get_async_session, metadata
from src.main import app
from src.settings import (
    BASE_DIR,
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
)

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
TEST_FILES_DIR = os.path.join(BASE_DIR, 'tests', 'test_audio')

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test

TEST_FILE_NAME = 'test'


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope='session')
def override_settings():
    TEMP_UPLOADS_DIR = tempfile.mkdtemp(dir=BASE_DIR)
    TEMP_MP3 = tempfile.mkdtemp(dir=TEMP_UPLOADS_DIR)
    TEMP_WAV = tempfile.mkdtemp(dir=TEMP_UPLOADS_DIR)

    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[get_mp3_folder] = lambda: TEMP_MP3
    app.dependency_overrides[get_wav_folder] = lambda: TEMP_WAV
    yield

    shutil.rmtree(TEMP_MP3)
    shutil.rmtree(TEMP_WAV)
    shutil.rmtree(TEMP_UPLOADS_DIR)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


client = TestClient(app)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
