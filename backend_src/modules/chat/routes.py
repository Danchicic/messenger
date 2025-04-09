import json

from fastapi import APIRouter, HTTPException, status
from starlette.websockets import WebSocket

from core.redis_conf import get_redis

router = APIRouter()


async def get_all_chats():
    redis_client = get_redis()
    chats = redis_client.lrange("chats", 0, -1)
    chats_resp = []
    for chat_info in chats:
        chat_info = json.loads(chat_info)
        chats_resp.append({
            "chat_name": chat_info["chat_name"],
            "messages": chat_info["messages"],
        })

    return chats_resp


async def check_chat_containing(chat_name: str, chats: list):
    for created_chat in chats:
        if created_chat['chat_name'] == chat_name:
            return True

    return False


@router.get("/health")
async def health():
    return {"status": "OK"}


@router.post("/create_chat")
async def create_chat(chat_name: str):
    redis_client = get_redis()
    chats = await get_all_chats()
    if await check_chat_containing(chat_name, chats):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='chat already exists'
        )
    redis_client.lpush("chats", json.dumps({
        "chat_name": chat_name,
        "messages": [],
    }))
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Chat created!")


@router.get("/chats")
async def list_chats():
    return {"chats": await get_all_chats()}


@router.websocket("/ws/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await websocket.accept()

    chats = await get_all_chats()
    if not (await check_chat_containing(chat_name, chats)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found!")

    await websocket.send_text(chats)
    while True:
        await websocket.receive_json()
