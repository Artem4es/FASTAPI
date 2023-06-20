import uvicorn
from fastapi import FastAPI

from audio.router import router as audio_router
from auth.router import router as auth_router

app = FastAPI()


app.include_router(auth_router, tags=["auth"])
app.include_router(audio_router, tags=["audio"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
