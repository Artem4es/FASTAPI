import os
import uuid

from httpx import AsyncClient

from tests.conftest import TEST_FILE_NAME, TEST_FILES_DIR



async def test_upload_wav(ac: AsyncClient):
    """Test .wav file uploading and downloading"""
    global id, user
    filename = TEST_FILE_NAME + '.wav'
    filepath = os.path.join(TEST_FILES_DIR, filename)
    with open(filepath, 'rb') as file:
        files = {'file': (filename, file)}
        token = dict(ac.cookies)
        response = await ac.post(
            url='/uploadfile/', files=files, cookies=token
        )
    assert response.status_code == 200, 'File upload unsucessfull'
    a = response.json().get('download_link')
    id, user = a.split('=')[1:3]
    id = id.split('&')[0]
    data = {
        "id": id,
        "user": user,
    }
    token = dict(ac.cookies)
    response = await ac.get(url="/record/", cookies=token, params=data)

    assert response.status_code == 200, 'File upload wasn\'t successfull'



async def test_upload_jpg(ac: AsyncClient):
    """Try to load jpg instead of wav"""
    filename = TEST_FILE_NAME + '.jpg'
    filepath = os.path.join(TEST_FILES_DIR, filename)
    with open(filepath, 'rb') as file:
        token = dict(ac.cookies)
        files = {'file': (filename, file)}
        response = await ac.post(
            url='/uploadfile/', files=files, cookies=token
        )
    assert response.status_code == 422, 'Image shouldn\'t be uploaded!'



async def test_upload_mp3(ac: AsyncClient):
    """Try to load mp3 instead of wav"""
    filename = TEST_FILE_NAME + '.mp3'
    filepath = os.path.join(TEST_FILES_DIR, filename)
    with open(filepath, 'rb') as file:
        token = dict(ac.cookies)
        files = {'file': (filename, file)}
        response = await ac.post(
            url='/uploadfile/', files=files, cookies=token
        )
    assert response.status_code == 422, 'mp3 shouldn\'t be uploaded!'


)
async def test_bad_download(ac: AsyncClient):
    """Try to download unexisting file"""

    data = {
        "id": uuid.uuid4(),
        "user": uuid.uuid4(),
    }

    token = dict(ac.cookies)
    response = await ac.get(url="/record/", cookies=token, params=data)

    assert response.status_code == 400, 'Unexisting file was downloaded'
    assert (
        response.json().get('detail') == 'У нас нет такого файла :('
    ), 'Wrong message for unexisting file'
