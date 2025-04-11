import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from database import init_models
from core.redis_conf import init_redis, close_redis
from database import async_session
from modules.chat.services import fill_users_sockets
from routes import main_router
from core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    try:
        os.makedirs(os.path.join(config.base_dir, "uploads"))
    except FileExistsError:
        pass
    init_redis()
    await init_models()
    await fill_users_sockets()
    yield
    close_redis()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def health():
    return {"status": "OK"}


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with async_session() as session:
        request.state.db = session
        response = await call_next(request)

        # If we got here without exceptions, commit any pending changes
        if hasattr(request.state, "db") and request.state.db.is_active:
            await request.state.db.commit()

        return response
