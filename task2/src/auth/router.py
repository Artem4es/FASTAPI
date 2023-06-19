from fastapi import APIRouter

from auth.manager import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
