from contextlib import asynccontextmanager

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.models import Base
from app.realtime import sio
from app.routers import auth, chats, messages, posts, test, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


fastapi_app = FastAPI(title="Estate Explorer API", lifespan=lifespan)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(auth.router)
fastapi_app.include_router(users.router)
fastapi_app.include_router(posts.router)
fastapi_app.include_router(chats.router)
fastapi_app.include_router(messages.router)
fastapi_app.include_router(test.router)

# Wrap the FastAPI app so Socket.IO is served on the same host/port
# (default path "/socket.io/"). ASGIApp forwards lifespan to other_asgi_app.
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
