from fastapi import APIRouter

from .chat.routes import router as chat_router
from .files.routes import router as files_router

main_router = APIRouter()
main_router.include_router(chat_router, tags=["chat"])
main_router.include_router(files_router, tags=["files"])
