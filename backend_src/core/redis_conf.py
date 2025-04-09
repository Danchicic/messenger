import redis
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()
_redis_client = None
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = 3


def init_redis():
    global _redis_client
    logger.debug(f'redis creds:{REDIS_HOST}:{REDIS_PORT}')
    _redis_client = redis.Redis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        db=REDIS_DB,
        decode_responses=True,
    )
    try:
        _redis_client.ping()
    except redis.exceptions.ConnectionError:
        logger.info("Redis is not running, try to run via brew")
        try:
            import subprocess
            subprocess.run(["brew", "services", "start", "redis"])
        except Exception:
            logger.info("cant start redis via brew")
            quit()
    logger.info("Redis connected")


def close_redis():
    global _redis_client
    if _redis_client:
        _redis_client.close()
        logger.warning("Redis disconnected")


def get_redis():
    global _redis_client
    if not _redis_client:
        init_redis()
    return _redis_client
