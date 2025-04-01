from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, AudioFile
from app.schemas import UserInDB, UserUpdate


async def get_user_by_id(db: AsyncSession, user_id: int):
    user = await db.execute(select(User).filter(User.id == user_id))
    return user.scalar_one_or_none()


async def get_user_by_yandex_id(db: AsyncSession, yandex_id: str):
    user = await db.execute(select(User).filter(User.yandex_id == yandex_id))
    return user.scalar_one_or_none()


async def create_user(db: AsyncSession, user: dict):
    db_user = User(**user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, db_user: UserInDB, user_update: UserUpdate):
    update_data = user_update.dict(exclude_unset=True)

    if not update_data:
        return db_user

    await db.execute(update(User).where(User.id == db_user.id).values(**update_data))
    await db.commit()

    result = await db.execute(select(User).where(User.id == db_user.id))
    return result.scalars().first()


async def delete_user(db: AsyncSession, db_user: UserInDB):
    await db.delete(db_user)
    await db.commit()


async def get_audio_files_by_user(db: AsyncSession, db_user: UserInDB, skip: int = 0, limit: int = 100):
    files = await db.execute(select(AudioFile).filter(AudioFile.owner_id == db_user.id).offset(skip).limit(limit))
    return files.scalars().all()


async def create_user_audio(db: AsyncSession, db_user: UserInDB, file_path: str, audio_data: dict):
    db_audio = AudioFile(**audio_data, file_path=file_path, owner_id=db_user.id)
    db.add(db_audio)
    await db.commit()
    await db.refresh(db_audio)
    return db_audio