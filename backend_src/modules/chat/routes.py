import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, HTTPException, status
from redis import Redis
from starlette.websockets import WebSocket, WebSocketDisconnect

from auth.jwt_module.depends import get_user_from_token
from core.config import users_sockets, config
from core.redis_conf import get_redis
from modules.chat import schemas
from modules.chat.services import get_all_chats, insert_event

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

    chats: dict[str, list[schemas.Message | schemas.File]] = await get_all_chats()
    # if not (await check_chat_containing(chat_name, chats)):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")
    # print("chats", chats)
    if chats.get(chat_name) is not None:
        messages: list[schemas.Message | schemas.File] = chats[chat_name]

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")

    token = await websocket.receive_text()
    if not (user := get_user_from_token(token)):
        raise HTTPException(status_code=401, detail="Invalid token!")
    # add new user socket to chat (subscribe user to new messages)
    users_sockets[chat_name]["sockets"].append(websocket)

    # send all prev messages
    await websocket.send_json(
        schemas.WSEventsExchanging(
            type="message",
            payload={
                "messages": messages
            }
        ).model_dump()
    )
    try:
        while True:
            # wait for text from users
            event_from_user: schemas.WSEventsExchanging = schemas.WSEventsExchanging(**(await websocket.receive_json()))
            print("ee", event_from_user)
            if event_from_user.type == "message":
                payload = event_from_user.payload
                message_from_user:str = payload["message"]
                # save message in db
                await insert_event(
                    schemas.Message(
                        type='text',
                        message=message_from_user,
                        user_phone=user.phone_number.phone_number,
                    ),
                    chat=chat_name,
                    redis=get_redis()
                )
                # send current message to all subscribed users
                message_to_send = schemas.WSEventsExchanging(
                    type="message",
                    payload={
                        "messages": [{
                            "type": "text",
                            "message": message_from_user,
                            "user_phone": user.phone_number.phone_number,
                        }]
                    }
                )

                for socket_to_send in users_sockets[chat_name]["sockets"]:
                    socket_to_send: WebSocket
                    await socket_to_send.send_json(message_to_send.model_dump())

            elif event_from_user.type == "file":
                event_data = event_from_user.payload

                file_data = event_data["file_data"]

                file_bytes = bytes(file_data['data'])
                file_name = f"{uuid.uuid4().hex[:20]}_{file_data['name'].replace(' ', '_')}"

                file_path = os.path.join(config.base_dir, "uploads", file_name)

                async with aiofiles.open(file_path, "wb+") as f:
                    await f.write(file_bytes)
                file_url = f"/uploads/{file_name}"
                await insert_event(
                    schemas.File(
                        type='file',
                        file_url=file_url,
                        file_name=file_name,
                        user_phone=user.phone_number.phone_number,
                    ),
                    chat=chat_name,
                    redis=get_redis()
                )

                for socket in users_sockets[chat_name]["sockets"]:
                    await socket.send_json(
                        schemas.WSEventsExchanging(
                            type="file",
                            payload={
                                "user_phone": user.phone_number.phone_number,
                                "file_name": file_name,
                                "file_url": file_url,
                                "payload": {
                                    "name": file_data['name'],
                                    "url": file_url
                                }
                            }
                        ).model_dump()
                    )

    except WebSocketDisconnect:
        users_sockets[chat_name]["sockets"].remove(websocket)
