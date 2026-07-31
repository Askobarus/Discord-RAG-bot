import logging
from dotenv import load_dotenv
import os

from bot import create_bot

# Загрузка переменных окружения
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Настройка логирования
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')

# Создание и запуск бота
bot = create_bot()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
