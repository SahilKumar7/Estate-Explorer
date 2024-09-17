import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, verify_token
from app.models import Chat, User, chat_participants
from app.schemas import ChatDetailOut, ChatOut, CreateChatRequest, MessageOut, ReceiverSnippet

router = APIRouter(prefix="/api/chats", tags=["chats"])


@router.get("/")
async def get_chats(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> list[ChatOut]:
    uid = uuid.UUID(user_id)

    result = await db.execute(
        select(Chat)
        .join(chat_participants, chat_participants.c.chat_id == Chat.id)
        .where(chat_participants.c.user_id == uid)
        .options(selectinload(Chat.users))
    )
    chats = result.scalars().unique().all()

    out: list[ChatOut] = []
    for chat in chats:
        receiver_user = next((u for u in chat.users if u.id != uid), None)
        receiver = ReceiverSnippet.model_validate(receiver_user) if receiver_user else None
        chat_out = ChatOut.model_validate(chat)
        chat_out.receiver = receiver
        out.append(chat_out)

    return out


@router.get("/{id}")
async def get_chat(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> ChatDetailOut:
    uid = uuid.UUID(user_id)

    result = await db.execute(
        select(Chat)
        .join(chat_participants, chat_participants.c.chat_id == Chat.id)
        .where(chat_participants.c.user_id == uid, Chat.id == id)
        .options(selectinload(Chat.messages), selectinload(Chat.users))
    )
    chat = result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")

    seen = list(set(chat.seen_by or []) | {uid})
    chat.seen_by = seen
    await db.commit()
    await db.refresh(chat)

    receiver_user = next((u for u in chat.users if u.id != uid), None)
    receiver = ReceiverSnippet.model_validate(receiver_user) if receiver_user else None

    detail = ChatDetailOut.model_validate(chat)
    detail.receiver = receiver
    detail.messages = [MessageOut.model_validate(m) for m in chat.messages]
    return detail


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_chat(
    body: CreateChatRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> ChatOut:
    uid = uuid.UUID(user_id)

    sender_result = await db.execute(select(User).where(User.id == uid))
    sender = sender_result.scalar_one_or_none()
    receiver_result = await db.execute(select(User).where(User.id == body.receiverId))
    receiver = receiver_result.scalar_one_or_none()

    if not sender or not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    chat = Chat()
    chat.users.append(sender)
    chat.users.append(receiver)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)

    chat_out = ChatOut.model_validate(chat)
    chat_out.receiver = ReceiverSnippet.model_validate(receiver)
    return chat_out


@router.put("/read/{id}")
async def read_chat(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> ChatOut:
    uid = uuid.UUID(user_id)

    result = await db.execute(
        select(Chat)
        .join(chat_participants, chat_participants.c.chat_id == Chat.id)
        .where(chat_participants.c.user_id == uid, Chat.id == id)
    )
    chat = result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")

    chat.seen_by = [uid]
    await db.commit()
    await db.refresh(chat)
    return ChatOut.model_validate(chat)
