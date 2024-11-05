import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, optional_token, verify_token
from app.models import ListingType, Post, PostDetail, PropertyType, SavedPost
from app.schemas import CreatePostRequest, PostOut, SinglePostOut

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/")
async def get_posts(
    db: AsyncSession = Depends(get_db),
    city: str | None = Query(default=None),
    type: ListingType | None = Query(default=None),
    property: PropertyType | None = Query(default=None),
    bedroom: int | None = Query(default=None),
    minPrice: int | None = Query(default=None),
    maxPrice: int | None = Query(default=None),
) -> list[PostOut]:
    stmt = select(Post)

    filters = []
    if city:
        filters.append(func.lower(Post.city) == city.lower())
    if type:
        filters.append(Post.type == type)
    if property:
        filters.append(Post.property == property)
    if bedroom:
        filters.append(Post.bedroom == bedroom)
    if minPrice is not None:
        filters.append(Post.price >= minPrice)
    if maxPrice is not None:
        filters.append(Post.price <= maxPrice)

    if filters:
        stmt = stmt.where(and_(*filters))

    result = await db.execute(stmt)
    return [PostOut.model_validate(p) for p in result.scalars().all()]


@router.get("/{id}")
async def get_post(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    maybe_user_id: str | None = Depends(optional_token),
) -> SinglePostOut:
    result = await db.execute(
        select(Post)
        .where(Post.id == id)
        .options(selectinload(Post.post_detail), selectinload(Post.user))
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    is_saved = False
    if maybe_user_id:
        uid = uuid.UUID(maybe_user_id)
        saved_result = await db.execute(
            select(SavedPost).where(and_(SavedPost.post_id == id, SavedPost.user_id == uid))
        )
        is_saved = saved_result.scalar_one_or_none() is not None

    out = SinglePostOut.model_validate(post)
    out.isSaved = is_saved
    return out


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_post(
    body: CreatePostRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> PostOut:
    post = Post(
        **body.postData.model_dump(),
        user_id=uuid.UUID(user_id),
    )
    db.add(post)
    await db.flush()

    detail = PostDetail(**body.postDetail.model_dump(), post_id=post.id)
    db.add(detail)

    await db.commit()
    await db.refresh(post)
    return PostOut.model_validate(post)


@router.put("/{id}")
async def update_post(
    id: uuid.UUID,
    body: CreatePostRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> PostOut:
    result = await db.execute(
        select(Post).where(Post.id == id).options(selectinload(Post.post_detail))
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    if str(post.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized!")

    post_data = body.postData.model_dump()
    for field, value in post_data.items():
        setattr(post, field, value)

    if post.post_detail:
        detail_data = body.postDetail.model_dump()
        for field, value in detail_data.items():
            setattr(post.post_detail, field, value)
    else:
        detail = PostDetail(**body.postDetail.model_dump(), post_id=post.id)
        db.add(detail)

    await db.commit()
    await db.refresh(post)
    return PostOut.model_validate(post)


@router.delete("/{id}")
async def delete_post(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    if str(post.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized!")

    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted"}
