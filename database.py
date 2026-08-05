from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy import text

DATABASE_URL = "sqlite+aiosqlite:///messages.db"
engine = create_async_engine(DATABASE_URL, echo=False)
new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase, MappedAsDataclass):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA synchronous=NORMAL;"))
        await conn.execute(text("PRAGMA cache_size=-32000;"))