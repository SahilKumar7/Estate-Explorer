import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class PropertyType(str, enum.Enum):
    apartment = "apartment"
    house = "house"
    condo = "condo"
    land = "land"


class ListingType(str, enum.Enum):
    buy = "buy"
    rent = "rent"


chat_participants = Table(
    "chat_participants",
    Base.metadata,
    Column("chat_id", UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    saved_posts = relationship("SavedPost", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", secondary=chat_participants, back_populates="users")


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    images = Column(ARRAY(String), default=list)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    bedroom = Column(Integer, nullable=False)
    bathroom = Column(Integer, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    type = Column(Enum(ListingType, name="listing_type"), nullable=False)
    property = Column(Enum(PropertyType, name="property_type"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="posts")
    post_detail = relationship("PostDetail", back_populates="post", uselist=False, cascade="all, delete-orphan")
    saved_posts = relationship("SavedPost", back_populates="post", cascade="all, delete-orphan")


class PostDetail(Base):
    __tablename__ = "post_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    desc = Column(Text, nullable=False)
    utilities = Column(String, nullable=True)
    pet = Column(String, nullable=True)
    income = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    school = Column(Integer, nullable=True)
    bus = Column(Integer, nullable=True)
    restaurant = Column(Integer, nullable=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), unique=True, nullable=False)

    post = relationship("Post", back_populates="post_detail")


class SavedPost(Base):
    __tablename__ = "saved_posts"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="saved_posts")
    post = relationship("Post", back_populates="saved_posts")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    seen_by = Column(ARRAY(UUID(as_uuid=True)), default=list)
    last_message = Column(String, nullable=True)

    users = relationship("User", secondary=chat_participants, back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    user_id = Column(String, nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chat = relationship("Chat", back_populates="messages")
