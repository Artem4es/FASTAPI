from httpx import AsyncClient

from tests.conftest import pytest


@pytest.mark.order(1)
async def test_register(ac: AsyncClient):
    """Test user register"""
    response = await ac.post(
        "/auth/register",
        json={
            "email": "s@s.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
        },
    )
    assert response.status_code == 201, 'User wasn\'t registered'


@pytest.mark.order(2)
async def test_fail_register(ac: AsyncClient):
    """Test user register"""
    response = await ac.post(
        "/auth/register",
        json={
            "email": "sssdcom",
            "password": "ssddssd",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "strddding",
        },
    )
    assert response.status_code == 422, 'Email validation error'


@pytest.mark.order(3)
async def test_user_auth(ac: AsyncClient):
    """User authentication test"""
    response = await ac.post(
        '/auth/jwt/login', data={"username": "s@s.com", "password": "string"}
    )
    assert response.status_code == 200, 'Authentication error'
    cookie = dict(response.cookies).get('fastapiusersauth')
    assert cookie is not None, 'Cookie hasn\'t been set'


@pytest.mark.order(4)
async def test_wrong_credentials(ac: AsyncClient):
    """Wrong auth data"""
    response = await ac.post(
        '/auth/jwt/login',
        data={"username": "abra@kadabra.com", "password": "hello"},
    )
    assert response.status_code == 400, 'Authenticated with wrong credentials!'
    cookie = dict(response.cookies).get('fastapiusersauth')
    assert cookie is None, 'Cookie has been set for not authenticated user'
