import sqlite_vec
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy import text
from models.messages import Base, MessageModel, ChunkModel


DATABASE_URL = "sqlite+aiosqlite:///messages.db"
engine = create_async_engine(DATABASE_URL, echo=False)
new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# 1. Автоматически загружаем расширение при каждом подключении
@event.listens_for(engine.sync_engine, "connect")
def load_sqlite_vec_extension(dbapi_conn, connection_record):
    # dbapi_conn здесь является объектом aiosqlite.Connection
    dbapi_conn.enable_load_extension(True)
    sqlite_vec.load(dbapi_conn)



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA synchronous=NORMAL;"))
        await conn.execute(text("PRAGMA cache_size=-32000;"))