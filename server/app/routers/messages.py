import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, verify_token
from app.models import Chat, Message, chat_participants
from app.schemas import AddMessageRequest, MessageOut

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post("/{chat_id}", status_code=status.HTTP_201_CREATED)
async def add_message(
    chat_id: uuid.UUID,
    body: AddMessageRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(verify_token),
) -> MessageOut:
    uid = uuid.UUID(user_id)

    result = await db.execute(
        select(Chat)
        .join(chat_participants, chat_participants.c.chat_id == Chat.id)
        .where(chat_participants.c.user_id == uid, Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")

    message = Message(text=body.text, chat_id=chat_id, user_id=user_id)
    db.add(message)

    chat.seen_by = [uid]
    chat.last_message = body.text
    await db.commit()
    await db.refresh(message)

    return MessageOut.model_validate(message)
