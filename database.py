from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy import text
from models.messages import Base, MessageModel, ChunkModel


DATABASE_URL = "sqlite+aiosqlite:///messages.db"
engine = create_async_engine(DATABASE_URL, echo=False)
new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        # Создаем FTS5-таблицу для полнотекстового поиска
        # tokenize="unicode61" поддерживает кириллицу
        await conn.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                content,
                channel_id,
                content='',
                tokenize='unicode61'
            );
        """))
        
        # Триггеры для автоматической синхронизации chunks <-> chunks_fts
        await conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, content, channel_id) 
                VALUES (new.id, new.content, new.channel_id);
            END;
        """))
        
        await conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content, channel_id) 
                VALUES('delete', old.id, old.content, old.channel_id);
            END;
        """))
        
        await conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content, channel_id) 
                VALUES('delete', old.id, old.content, old.channel_id);
                INSERT INTO chunks_fts(rowid, content, channel_id) 
                VALUES (new.id, new.content, new.channel_id);
            END;
        """))
        
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA synchronous=NORMAL;"))
        await conn.execute(text("PRAGMA cache_size=-32000;"))