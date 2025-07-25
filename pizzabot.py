import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from admins import dialogs as admin_dialogs
from admins.states import MainSG as admin_mainsg
from config import Roles, settings
from couriers.states import MainSG as courier_mainsg
from db.models import User
from middlewares import DbSessionMiddleware
from routers import router

engine = create_async_engine(settings.sqlite_async_dsn, echo=False)


async def ui_error_handler(event: ErrorEvent, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    userid = dialog_manager.middleware_data["event_from_user"].id
    user = await session.get(User, userid)
    start_state = admin_mainsg.main if user.role == Roles.ADMIN else courier_mainsg.main
    await dialog_manager.start(state=start_state, mode=StartMode.RESET_STACK)
    logging.warning("Сброс ошибки: {event}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    db_pool = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage = RedisStorage(
        Redis(),
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
            with_bot_id=True,
        ),
    )
    dp = Dispatcher(storage=storage)
    dp.include_routers(router, admin_dialogs.add_user)
    setup_dialogs(dp)
    dp.update.outer_middleware(DbSessionMiddleware(db_pool))
    dp.errors.register(
        ui_error_handler,
        ExceptionTypeFilter(UnknownIntent, OutdatedIntent),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
