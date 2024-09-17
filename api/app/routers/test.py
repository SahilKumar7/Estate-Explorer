from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from jose import JWTError, jwt

from app.config import settings
from app.dependencies import verify_token

router = APIRouter(prefix="/api/test", tags=["test"])


@router.get("/should-be-logged-in")
async def should_be_logged_in(user_id: str = Depends(verify_token)):
    return {"message": "You are Authenticated"}


@router.get("/should-be-admin")
async def should_be_admin(token: str | None = Cookie(default=None)):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated!")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not Valid!")

    if not payload.get("isAdmin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized!")

    return {"message": "You are Authenticated"}
