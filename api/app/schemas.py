from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models import ListingType, PropertyType


class CamelModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


# ── User ──────────────────────────────────────────────────────────────────────

class UserOut(CamelModel):
    id: uuid.UUID
    email: str
    username: str
    avatar: str | None = None
    created_at: datetime


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    avatar: str | None = None


# ── Post ──────────────────────────────────────────────────────────────────────

class PostDetailIn(BaseModel):
    desc: str
    utilities: str | None = None
    pet: str | None = None
    income: str | None = None
    size: int | None = None
    school: int | None = None
    bus: int | None = None
    restaurant: int | None = None


class PostDetailOut(PostDetailIn, CamelModel):
    id: uuid.UUID


class PostDataIn(BaseModel):
    title: str
    price: int
    images: list[str] = []
    address: str
    city: str
    bedroom: int
    bathroom: int
    latitude: str
    longitude: str
    type: ListingType
    property: PropertyType


class CreatePostRequest(BaseModel):
    postData: PostDataIn
    postDetail: PostDetailIn


class PostOut(CamelModel):
    id: uuid.UUID
    title: str
    price: int
    images: list[str]
    address: str
    city: str
    bedroom: int
    bathroom: int
    latitude: str
    longitude: str
    type: ListingType
    property: PropertyType
    created_at: datetime
    user_id: uuid.UUID


class PostUserSnippet(CamelModel):
    id: uuid.UUID
    username: str
    avatar: str | None = None


class SinglePostOut(PostOut):
    post_detail: PostDetailOut | None = None
    user: PostUserSnippet | None = None
    isSaved: bool = False


# ── SavedPost / Profile Posts ─────────────────────────────────────────────────

class SavePostRequest(BaseModel):
    postId: uuid.UUID


class ProfilePostsOut(BaseModel):
    userPosts: list[PostOut]
    savedPosts: list[PostOut]


# ── Chat ──────────────────────────────────────────────────────────────────────

class ReceiverSnippet(CamelModel):
    id: uuid.UUID
    username: str
    avatar: str | None = None


class ChatOut(CamelModel):
    id: uuid.UUID
    created_at: datetime
    seen_by: list[uuid.UUID]
    last_message: str | None = None
    receiver: ReceiverSnippet | None = None


class ChatDetailOut(ChatOut):
    messages: list[MessageOut] = []


class CreateChatRequest(BaseModel):
    receiverId: uuid.UUID


# ── Message ───────────────────────────────────────────────────────────────────

class MessageOut(CamelModel):
    id: uuid.UUID
    text: str
    user_id: str
    chat_id: uuid.UUID
    created_at: datetime


class AddMessageRequest(BaseModel):
    text: str


# Rebuild forward refs so ChatDetailOut can use MessageOut
ChatDetailOut.model_rebuild()
