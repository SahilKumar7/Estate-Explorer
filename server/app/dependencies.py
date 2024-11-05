from typing import AsyncGenerator

from fastapi import Cookie, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def verify_token(token: str | None = Cookie(default=None)) -> str:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated!")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id: str | None = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not Valid!")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not Valid!")


def optional_token(token: str | None = Cookie(default=None)) -> str | None:
    """Return user_id if a valid token is present, otherwise None."""
    if token is None:
        return None
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload.get("id")
    except JWTError:
        return None
