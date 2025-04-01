from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


async def get_user(db: AsyncSession, user_id: int):
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