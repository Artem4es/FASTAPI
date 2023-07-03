import os

from httpx import AsyncClient

from src.settings import BASE_DIR
from tests.conftest import pytest


@pytest.mark.run(4)
async def test_upload_wav(ac: AsyncClient):
    """Test .wav file uploading"""
    filename = 'test.wav'
    filepath = os.path.join(BASE_DIR, 'tests', 'test_audio', filename)
    with open(filepath, 'rb') as file:
        files = {'file': (filename, file)}
        token = dict(ac.cookies)
        response = await ac.post(
            url='/uploadfile/', files=files, cookies=token
        )
    assert response.status_code == 200, 'File upload unsucessfull'


@pytest.mark.run(5)
async def test_upload_jpg(ac: AsyncClient):
    """Try to load jpg instead of wav"""
    filename = 'test.jpg'
    filepath = os.path.join(BASE_DIR, 'tests', 'test_audio', filename)
    with open(filepath, 'rb') as file:
        token = dict(ac.cookies)
        files = {'file': (filename, file)}
        response = await ac.post(
            url='/uploadfile/', files=files, cookies=token
        )
    assert response.status_code == 422, 'Image shouldn\'t be uploaded!'


@pytest.mark.run(6)
async def test_upload_mp3(ac: AsyncClient):
    """Try to load mp3 instead of wav"""
    filename = 'test.mp3'
    filepath = os.path.join(BASE_DIR, 'tests', 'test_audio', filename)
    with open(filepath, 'rb') as file:
        token = dict(ac.cookies)
        files = {'file': (filename, file)}
        response = await ac.post(
            url='/uploadfile/', files=files, cookies=token
        )
    assert response.status_code == 422, 'mp3 shouldn\'t be uploaded!'
