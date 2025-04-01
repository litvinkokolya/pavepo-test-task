import httpx
from fastapi import HTTPException
from app.core.config import settings

async def get_yandex_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"OAuth {access_token}"}
        try:
            response = await client.get(
                "https://login.yandex.ru/info",
                headers=headers,
                params={"format": "json"}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=400,
                detail="Could not validate credentials with Yandex"
            )

async def get_yandex_access_token(code: str):
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.YANDEX_CLIENT_ID,
            "client_secret": settings.YANDEX_CLIENT_SECRET
        }
        try:
            response = await client.post(
                "https://oauth.yandex.ru/token",
                data=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=400,
                detail="Could not get access token from Yandex"
            )