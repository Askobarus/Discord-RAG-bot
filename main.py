import asyncio
import logging
from dotenv import load_dotenv
import os

from bot import create_bot
from database import init_db

async def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    #handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')

    await init_db()
    print("База данных инициализирована")

    bot = create_bot()
    await bot.start(token)#, log_handler=handler, log_level=logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(main())