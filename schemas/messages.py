from pydantic import BaseModel, Field
from datetime import datetime

class SMessageBase(BaseModel):
    id: int
    channel_id: int
    author: str
    content: str
    timestamp: datetime

    model_config = {"from_attributes": True}

class SMessage(SMessageBase):
    pass