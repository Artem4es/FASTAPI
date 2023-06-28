from conftest import client


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "s@s.ru",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
        },
    )

    assert response.status_code == 201
