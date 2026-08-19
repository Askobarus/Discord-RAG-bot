from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SMessageBase(BaseModel):
    id: int
    channel_id: int
    author: str
    content: str
    timestamp: datetime

    model_config = {"from_attributes": True}

class SMessage(SMessageBase):

    @classmethod
    def from_discord_message(cls, message, channel_id:int) -> Optional['SMessage']:
        """Создает объект из Discord Message, если сообщение не пустое"""
        if not message.content.strip():
            return None
        
        return cls(
            id=message.id,
            channel_id=channel_id,
            author=message.author.name,
            content=message.content,
            timestamp=message.created_at
        )