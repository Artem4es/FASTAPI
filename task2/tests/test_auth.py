from conftest import async_session_maker
from httpx import AsyncClient
from sqlalchemy import select

from auth.models import User


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
    assert response.status_code == 201, 'User wasn\'t register'
    async with async_session_maker() as session:
        stmt = select(User)
        response = await session.execute(stmt)
        result = response.all()[0]
        assert len(result) == 1, 'Not right number of users was created'
        user = result[0]
        assert user.email == "s@s.com", 'Email created is wrong'
        assert user.username == "string", "Username created is wrong"


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


async def test_user_auth(ac: AsyncClient):
    """User authentication test"""
    response = await ac.post(
        '/auth/jwt/login', data={"username": "s@s.com", "password": "string"}
    )
    assert response.status_code == 200, 'Authentication error'
    cookie = dict(response.cookies).get('fastapiusersauth')
    assert cookie is not None, 'Cookie hasn\'t been set'


async def test_wrong_credentials(ac: AsyncClient):
    """Wrong auth data"""
    response = await ac.post(
        '/auth/jwt/login',
        data={"username": "abra@kadabra.com", "password": "hello"},
    )
    assert response.status_code == 400, 'Authenticated with wrong credentials!'
    cookie = dict(response.cookies).get('fastapiusersauth')
    assert cookie is None, 'Cookie has been set for not authenticated user'
