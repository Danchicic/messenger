from fastapi import APIRouter

from .chat import routes

main_router = APIRouter()
main_router.include_router(routes.router, tags=["chat"])
