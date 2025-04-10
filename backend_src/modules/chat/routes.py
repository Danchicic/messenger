import json
import logging

from fastapi import APIRouter, HTTPException, status
from redis import Redis
from starlette.websockets import WebSocket, WebSocketDisconnect

from auth.jwt_module.depends import get_user_from_token
from core.config import users_sockets
from core.redis_conf import get_redis
from modules.chat.services import get_all_chats, insert_message

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/chats")
async def list_chats():
    return {"chats": await get_all_chats()}


@router.post("/create_chat")
async def create_chat(chat_name: str):
    redis_client: Redis = get_redis()

    redis_client.hset(
        chat_name,
        key="messages",
        value="[]"
    )
    users_sockets[chat_name] = {
        "sockets": [],
    }
    # logger.info(f"{chat_name} created, {users_sockets}")
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Chat created!")


@router.websocket("/ws/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await websocket.accept()

    chats = await get_all_chats()
    # if not (await check_chat_containing(chat_name, chats)):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")
    # print("chats", chats)
    if chats.get(chat_name) is not None:
        messages = chats[chat_name]

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")

    token = await websocket.receive_text()
    if not (user := get_user_from_token(token)):
        raise HTTPException(status_code=401, detail="Invalid token!")
    # add new user socket to chat (subscribe user to new messages)
    users_sockets[chat_name]["sockets"].append(websocket)
    # send all prev messages
    await websocket.send_text(json.dumps(messages))
    try:
        while True:
            # wait for text from users
            event_from_user = await websocket.receive_json()
            if event_from_user.get("type") == "message":
                message_from_user = event_from_user["message"]
                # save message in db
                await insert_message(
                    message_from_user,
                    chat_name,
                    user.phone_number.phone_number,
                    get_redis()
                )
                # send current message to all subscribed users
                for socket_to_send in users_sockets[chat_name]["sockets"]:
                    socket_to_send: WebSocket
                    await socket_to_send.send_text(json.dumps([{
                        "message": message_from_user,
                        "user_phone": user.phone_number.phone_number,
                    }]))
            elif event_from_user.get("type") == "file":
                pass
    except WebSocketDisconnect:
        users_sockets[chat_name]["sockets"].remove(websocket)
