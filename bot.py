import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiosql import create_table
from hadlers import router
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await create_table()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Ваш бот выключен")