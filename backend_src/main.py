import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from database import init_models
from core.redis_conf import init_redis, close_redis
from database import async_session
from routes import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    init_redis()
    await init_models()
    yield
    close_redis()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    print("cc", request.cookies)
    async with async_session() as session:
        request.state.db = session
        response = await call_next(request)

        # If we got here without exceptions, commit any pending changes
        if hasattr(request.state, "db") and request.state.db.is_active:
            await request.state.db.commit()

        return response
