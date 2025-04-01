from fastapi import FastAPI

from app.api import audio, users
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router, prefix="/api/v1/users")
# app.include_router(audio.router, prefix="/api/v1/audio")