from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_db
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_MAX_AGE = 7 * 24 * 60 * 60  # 7 days in seconds


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    hashed = pwd_context.hash(body.password)
    user = User(username=body.username, email=body.email, password=hashed)
    db.add(user)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user!")
    return {"message": "User created successfully"}


@router.post("/login")
async def login(body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == body.username))
    user = result.scalar_one_or_none()

    if user is None or not pwd_context.verify(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials!")

    token = jwt.encode(
        {"id": str(user.id), "isAdmin": False, "exp": datetime.now(timezone.utc) + timedelta(days=7)},
        settings.JWT_SECRET_KEY,
        algorithm="HS256",
    )

    response.set_cookie(key="token", value=token, httponly=True, max_age=TOKEN_MAX_AGE)

    user_out = UserOut.model_validate(user)
    return user_out


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return {"message": "Logout Successful"}
