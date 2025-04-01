from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_current_user
from app.db import get_db
from app.schemas import UserInDB, AudioFileCreate, AudioFileInDB
from app.sevices.crud import get_audio_files_by_user, create_user_audio

router = APIRouter()

@router.get("/list_of_user")
async def get_files_by_user(db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user),
                            skip: int = 0, limit: int = 100):
    return await get_audio_files_by_user(db, current_user)


@router.post("/upload/", response_model=AudioFileInDB)
async def upload_audio_file(
        name: str,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in (".mp3", ".wav", ".ogg", ".flac"):
        raise HTTPException(status_code=400, detail="Unsupported file format. Need audio!")

    user_audio_dir = Path(settings.AUDIO_FILES_DIR) / str(current_user.id)
    user_audio_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{name}{file_ext}"
    file_path = user_audio_dir / file_name

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    audio_in = AudioFileCreate(name=name)
    audio_data = audio_in.dict()
    audio_info = await create_user_audio(db, current_user, str(file_path), audio_data)

    return audio_info