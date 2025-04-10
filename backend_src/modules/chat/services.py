import json
import logging

from core.redis_conf import get_redis
from core.config import users_sockets

logger = logging.getLogger(__name__)


async def insert_message(message: str, chat: str, user_phone: str, redis):
    chat_messages_list = json.loads(redis.hget(chat, "messages"))
    chat_messages_list.append(
        {
            "message": message,
            "user_phone": user_phone
        }
    )
    redis.hset(chat, "messages", json.dumps(chat_messages_list))


async def get_all_chats() -> dict:
    redis_client = get_redis()
    chats_resp = {}
    for chat in redis_client.scan_iter():
        # print(chat)
        try:
            chat_messages = redis_client.hget(chat, "messages")
            chats_resp[chat] = json.loads(chat_messages)
        except:
            logger.exception("Failed to get chat messages from redis")
            continue
    return chats_resp


async def fill_users_sockets():
    chats = await get_all_chats()
    for chat_name in chats.keys():
        users_sockets[chat_name] = {
            "sockets": [],
        }
