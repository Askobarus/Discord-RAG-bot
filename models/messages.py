from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy import Index, String, LargeBinary
from datetime import datetime


class Base(DeclarativeBase, MappedAsDataclass):
    pass

class MessageModel(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(index=True)
    author: Mapped[str]
    content: Mapped[str]
    timestamp: Mapped[datetime]
       
class ChunkModel(Base):
    __tablename__ = 'chunks'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(String(50))
    message_ids: Mapped[str] = mapped_column(String(500)) # "123,124,125"
    content: Mapped[str] = mapped_column(String(4000))    # Склеенный текст диалога
    embedding: Mapped[bytes] = mapped_column(LargeBinary) # Вектор как BLOB