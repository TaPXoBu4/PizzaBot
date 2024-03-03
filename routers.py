import asyncio

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from db.service import UserService
from states import AdminMainSG, CourierMainSG

start_router = Router()

START_STATES = {
    'admin': AdminMainSG.main,
    'courier': CourierMainSG.main
}


@start_router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    user = UserService.get_user(message.from_user.id)[0]

    if not user:
        admins = UserService.get_users_by_status('admin')
        bot: Bot = dialog_manager.middleware_data['bot']
        for admin in admins:
            await bot.send_message(admin['id'], f'{message.from_user.full_name, message.from_user.id} запустил бота')

        await message.reply('Администратор уведомлен о Вас, скоро Вы получите доступ к рабочему меню.')
        await asyncio.sleep(60)

        while True:
            user = UserService.get_user(message.from_user.id)[0]
            if user:
                break
            await asyncio.sleep(10)
    await dialog_manager.start(state=START_STATES[user['status']], mode=StartMode.RESET_STACK)
