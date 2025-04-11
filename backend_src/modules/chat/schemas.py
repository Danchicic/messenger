from pydantic import BaseModel


class WSEvent(BaseModel):
    type: str
    user_phone: str


class Message(WSEvent):
    message: str


class File(WSEvent):
    file_name: str
    file_url: str


class WSEventsExchanging(BaseModel):
    type: str
    payload: dict
