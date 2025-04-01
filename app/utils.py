from typing import Literal

import jwt
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


async def decode_token(
        token: str,
        expected_type: Literal["access", "refresh"] | None = None,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if expected_type and payload.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Expected {expected_type} token",
            )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )