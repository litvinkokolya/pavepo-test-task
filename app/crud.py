from select import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models import User


async def get_user(db: AsyncSession, user_id: int):
    user = await db.execute(select(User).filter(User.id == user_id))
    return user.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    user = await db.execute(select(User).filter(User.email == email))
    return user.scalar_one_or_none()

async def get_user_by_yandex_id(db: AsyncSession, yandex_id: str):
    user = await db.execute(select(User).filter(User.yandex_id == yandex_id))
    return user.scalar_one_or_none()

async def create_user(db: AsyncSession, user: dict):
    password = user.pop('password', None)
    if password:
        hashed_password = get_password_hash(password)
        db_user = User(**user, hashed_password=hashed_password)
    else:
        db_user = User(**user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user