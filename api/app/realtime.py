import socketio

from app.config import settings

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[settings.CLIENT_URL])

online_users: list[dict] = []


def add_user(user_id, sid):
    if not any(user["user_id"] == user_id for user in online_users):
        online_users.append({"user_id": user_id, "sid": sid})


def remove_user(sid):
    global online_users
    online_users = [user for user in online_users if user["sid"] != sid]


def get_user(user_id):
    for user in online_users:
        if user["user_id"] == user_id:
            return user
    return None


@sio.event
async def connect(sid, environ):
    pass  # Connection established


@sio.event
async def newUser(sid, user_id):
    add_user(user_id, sid)


@sio.event
async def sendMessage(sid, data):
    receiver_id = data.get("receiverId")
    message_data = data.get("data")
    receiver = get_user(receiver_id)
    if receiver:
        await sio.emit("getMessage", message_data, to=receiver["sid"])


@sio.event
async def disconnect(sid):
    remove_user(sid)
