from datetime import datetime, timedelta
from typing import Literal
import jwt

from fastapi.params import Security
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.sevices.crud import get_user_by_yandex_id
from app.db import get_db
from app.schemas import UserInDB
from app.utils import decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


def create_token(data: dict, expires_delta: timedelta, token_type: Literal["access", "refresh"]) -> str:
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    to_encode.update({"type": token_type})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Security(security),
) -> UserInDB:
    payload = await decode_token(credentials.credentials, expected_type="access")
    yandex_id = payload.get("sub")

    if not yandex_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_yandex_id(db, yandex_id=yandex_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def get_superuser(user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return user