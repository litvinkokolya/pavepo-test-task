from fastapi import FastAPI

from app.api import audio, users
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations with users",
        },
        {
            "name": "Audio",
            "description": "Operations with audio files",
        }
    ]
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(audio.router, prefix="/api/v1/audio", tags=["Audio"])