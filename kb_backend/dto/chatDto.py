from pydantic import BaseModel


class SendChatRequest(BaseModel):
    chatRoomId: str
    content: str
