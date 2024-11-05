import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, verify_token
from app.models import Chat, Post, SavedPost, User, chat_participants
from app.schemas import (
    ProfilePostsOut,
    PostOut,
    SavePostRequest,
    UserOut,
    UserUpdate,
)

router = APIRouter(prefix="/api/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)) -> list[UserOut]:
    result = await db.execute(select(User))
    return [UserOut.model_validate(u) for u in result.scalars().all()]


@router.put("/{id}")
async def update_user(
    id: uuid.UUID,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
):
    if str(id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized!")

    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    update_data = body.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        update_data["password"] = pwd_context.hash(update_data["password"])
    else:
        update_data.pop("password", None)

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)


@router.delete("/{id}")
async def delete_user(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
):
    if str(id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized!")

    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}


@router.post("/save")
async def save_post(
    body: SavePostRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
):
    uid = uuid.UUID(user_id)
    result = await db.execute(
        select(SavedPost).where(and_(SavedPost.user_id == uid, SavedPost.post_id == body.postId))
    )
    existing = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        await db.commit()
        return {"message": "Post removed from saved list"}

    saved = SavedPost(user_id=uid, post_id=body.postId)
    db.add(saved)
    await db.commit()
    return {"message": "Post saved"}


@router.get("/profilePosts")
async def profile_posts(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> ProfilePostsOut:
    uid = uuid.UUID(user_id)

    user_posts_result = await db.execute(select(Post).where(Post.user_id == uid))
    user_posts = [PostOut.model_validate(p) for p in user_posts_result.scalars().all()]

    saved_result = await db.execute(
        select(SavedPost).where(SavedPost.user_id == uid).options(selectinload(SavedPost.post))
    )
    saved_posts = [PostOut.model_validate(sp.post) for sp in saved_result.scalars().all()]

    return ProfilePostsOut(userPosts=user_posts, savedPosts=saved_posts)


@router.get("/notification")
async def get_notification_number(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
):
    uid = uuid.UUID(user_id)

    count_result = await db.execute(
        select(func.count(Chat.id))
        .join(chat_participants, chat_participants.c.chat_id == Chat.id)
        .where(
            and_(
                chat_participants.c.user_id == uid,
                ~Chat.seen_by.any(uid),
            )
        )
    )
    count = count_result.scalar_one()
    return count
