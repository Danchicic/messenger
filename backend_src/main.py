from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from modules import main_router

app = FastAPI()

app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)
