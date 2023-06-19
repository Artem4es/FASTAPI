"""File with settings and configs for the project"""

import os
from pathlib import Path

from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)  # connect string for the database


BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = os.path.join(BASE_DIR, 'uploads')
