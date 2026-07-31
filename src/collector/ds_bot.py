import discord
import json
from datetime import datetime
from config.settings import DS_BOT_TOKEN, TARGET_CHANNEL_ID, RAW_DATA_DIR

class DiscordCollector:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
    
    async def collect(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')
            channel = self.client.get_channel(TARGET_CHANNEL_ID)
            
            if channel is None:
                print("CHANNEL UNAVAILABLE! CHECK CHANNEL ID AND BOT PERMISSIONS.")
                await self.client.close()
                return
            
            # Сбор истории (если нужно выкачать старую)
            messages = []
            async for message in channel.history(limit=None): # limit=None - вся история
                # Пропускаем пустые сообщения или команды ботов
                if not message.content or message.author.bot:
                    continue
                    
                messages.append({
                    "id": str(message.id),
                    "author": message.author.name,
                    "content": message.content,
                    "timestamp": message.created_at.isoformat(),
                    "reply_to": str(message.reference.message_id) if message.reference else None,
                    "thread_id": str(message.channel.id) if isinstance(message.channel, discord.Thread) else None
                })
                
            # Сохраняем
            RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
            output_file = RAW_DATA_DIR / f"discord_{TARGET_CHANNEL_ID}_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
                
            print(f"Saved {len(messages)} messages in {output_file}")
            await self.client.close()
        
        await self.client.start(DS_BOT_TOKEN)
            
if __name__ == "__main__":
    import asyncio
    collector = DiscordCollector()
    asyncio.run(collector.collect())