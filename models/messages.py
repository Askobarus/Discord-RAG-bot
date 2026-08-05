from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index
from datetime import datetime
from database import Base

class MessageModel(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(index=True)
    author: Mapped[str]
    content: Mapped[str]
    timestamp: Mapped[datetime]