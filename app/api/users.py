from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token, get_current_user
from app.crud import get_user_by_yandex_id, create_user
from app.db import get_db
from app.schemas import UserCreate
from app.sevices.yandex_auth import get_yandex_access_token, get_yandex_user_info

router = APIRouter()


@router.post("/yandex-aufth")
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

    access_token = create_token(data={"sub": db_user.yandex_id}, expires_delta=timedelta(minutes=15))
    refresh_token = create_token(data={"sub": db_user.yandex_id}, expires_delta=timedelta(days=3))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/update_token")
async def update_access_token(
        refresh_token: str,
        db: AsyncSession = Depends(get_db)
):
    try:
        user = await get_current_user(db, refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired refresh token"
        )

    new_access_token = create_token(
        data={"sub": user.yandex_id},
        expires_delta=timedelta(minutes=15)
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



# @router.get("/me", response_model=UserInDB)
# async def read_user_me(current_user: UserInDB = Depends(get_current_active_user)):
#     return current_user
#
#
# @router.put("/me", response_model=UserInDB)
# async def update_user_me(
#         user_in: UserUpdate,
#         db: Session = Depends(get_db),
#         current_user: UserInDB = Depends(get_current_active_user)
# ):
#     return update_user(db, db_user=current_user, user_in=user_in)
#
#
# @router.get("/users/", response_model=List[UserInDB])
# async def read_users(
#         skip: int = 0,
#         limit: int = 100,
#         db: Session = Depends(get_db),
#         current_user: UserInDB = Depends(get_current_active_superuser)
# ):
#     users = get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @router.delete("/users/{user_id}")
# async def delete_user_by_id(
#         user_id: int,
#         db: Session = Depends(get_db),
#         current_user: UserInDB = Depends(get_current_active_superuser)
# ):
#     delete_user(db, user_id=user_id)
#     return {"message": "User deleted successfully"}