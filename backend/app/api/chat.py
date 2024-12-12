from fastapi import APIRouter
from noovox.core import chat
from pydantic import BaseModel

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    response = chat(chat_message.message)
    return {"response": response}
