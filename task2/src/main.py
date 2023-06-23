from fastapi import FastAPI

from audio.router import router as audio_router
from auth.router import router as auth_router

app = FastAPI()


app.include_router(auth_router, tags=["auth"])
app.include_router(audio_router, tags=["audio"])
