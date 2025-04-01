from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token, get_current_user, get_superuser
from app.sevices.crud import get_user_by_yandex_id, create_user, update_user, get_user_by_id, delete_user
from app.db import get_db
from app.schemas import UserCreate, UserInDB, UserUpdate
from app.sevices.yandex_auth import get_yandex_access_token, get_yandex_user_info
from app.utils import decode_token

router = APIRouter()


@router.get("/yandex-auth")
async def auth_via_yandex(code: str, db: AsyncSession = Depends(get_db)):
    token_data = await get_yandex_access_token(code)
    access_token = token_data["access_token"]

    yandex_user = await get_yandex_user_info(access_token)
    yandex_id = yandex_user["id"]
    email = yandex_user["default_email"]
    full_name = yandex_user["real_name"]

    db_user = await get_user_by_yandex_id(db, yandex_id=yandex_id)
    if not db_user:
        user_in = UserCreate(
            email=email,
            full_name=full_name,
            yandex_id=yandex_id
        )
        db_user = await create_user(db, user_in.dict())

    access_token = create_token(data={"sub": db_user.yandex_id}, expires_delta=timedelta(minutes=15), token_type="access")
    refresh_token = create_token(data={"sub": db_user.yandex_id}, expires_delta=timedelta(days=3), token_type="refresh")

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/update_token")
async def update_access_token(
        refresh_token: str,
        db: AsyncSession = Depends(get_db),
):
    payload = await decode_token(refresh_token, expected_type="refresh")
    yandex_id = payload.get("sub")

    user = await get_user_by_yandex_id(db, yandex_id=yandex_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_token(
        data={"sub": user.yandex_id},
        expires_delta=timedelta(minutes=15),
        token_type="access",
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }



@router.get("/me", response_model=UserInDB)
async def read_current_user(
    current_user: UserInDB = Depends(get_current_user)
):
    return current_user


@router.put("/me", response_model=UserInDB)
async def update_user_me(
        user_in: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    updated_user = await update_user(db, db_user=current_user, user_update=user_in)
    return updated_user


@router.delete("/{user_id}")
async def delete_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        super_user: UserInDB = Depends(get_superuser)
):
    user = await get_user_by_id(db, user_id)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await delete_user(db, user)

    return {"message": "User deleted successfully"}
