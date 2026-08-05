import logging
from sqlalchemy.dialects.sqlite import insert
from database import new_session
from models.messages import MessageModel

logger = logging.getLogger(__name__)

async def save_messages(messages_data: list[dict]) -> int:
    if not messages_data:
        return 0

    try:
        async with new_session() as session:
            stmt = insert(MessageModel).values(messages_data)
            
            stmt = stmt.on_conflict_do_update(
                index_elements=['id'],
                set_={
                    'content': stmt.excluded.content,
                    'author': stmt.excluded.author,
                    'timestamp': stmt.excluded.timestamp,
                    'channel_id': stmt.excluded.channel_id
                }
            )
            
            await session.execute(stmt)
            await session.commit()
            
        return len(messages_data)
    
    except Exception as e:
        logger.error(f"Критическая ошибка при сохранении сообщений в БД: {e}")
        raise

"""
# --- Бонус: функция для будущего RAG ---
async def get_messages_by_channel(channel_id: int, limit: int = 1000) -> list[dict]:
    
    #Получает последние сообщения из конкретного канала для RAG.
    
    from sqlalchemy import select, desc
    
    async with new_session() as session:
        stmt = (
            select(MessageModel)
            .where(MessageModel.channel_id == channel_id)
            .order_by(desc(MessageModel.timestamp))
            .limit(limit)
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()
        
        # Преобразуем ORM-объекты в словари (или Pydantic-схемы)
        return [{
            "id": msg.id,
            "author": msg.author,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        } for msg in messages]
"""