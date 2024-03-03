import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio.client import Redis

import config
import routers
from dialogs import admin, courier

async def main():
    bot = Bot(config.TOKEN)
    storage = RedisStorage(Redis(), key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True))
    dp = Dispatcher(storage=storage)
    dp.include_router(routers.start_router)
    dp.include_routers(courier.main_dialog, courier.new_order_dialog)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())