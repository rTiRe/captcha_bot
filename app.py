import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config.settings import settings
from handlers import router
from messages import _fill_data

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await _fill_data()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
