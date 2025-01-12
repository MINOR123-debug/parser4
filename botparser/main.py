import sys
import asyncio
import logging
import os
import signal
import schedule
import time
from aiogram import Bot, Dispatcher
from config import TOKEN

from handlers.command_handlers import command_router
from help import router
from rik import routeradm
from creit import creit_router
from admin import router11
from parser2 import parser_router, setup_telethon

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для перезапуску бота
def restart_bot():
    logger.info("Перезапуск бота...")
    os.kill(os.getpid(), signal.SIGINT)  # Завершує поточний процес (зупиняє бота)

# Функція для налаштування перезапуску через годину
def schedule_restart():
    schedule.every(1).hours.do(restart_bot)  # Перезапуск кожну годину

    while True:
        schedule.run_pending()  # Перевіряє, чи потрібно щось виконати
        time.sleep(1)

async def main():
    # Ініціалізація Telethon (перенесено в окрему функцію)
    await setup_telethon()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Підключення роутерів
    dp.include_router(parser_router)
    dp.include_router(command_router)
    dp.include_router(router)
    dp.include_router(routeradm)
    dp.include_router(creit_router)
    dp.include_router(router11)

    logger.info("Бот запускається...")

    # Запускаємо в окремому потоці функцію для перезапуску бота
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, schedule_restart)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка під час роботи бота: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        # Використовуємо asyncio.run() для основного циклу
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот вимкнено вручну.")
