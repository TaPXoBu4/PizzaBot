from enum import StrEnum

from admins.states import AddUserSG
from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode
from config import Roles, StartStates
from db.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

router = Router()


class UserActions(StrEnum):
    ADD = "add"
    BAN = "ban"
    PASS = "pass"


class UserActionCb(CallbackData, prefix="user_action"):
    action: str
    user_id: int | None = None


@router.message(CommandStart())
async def start_nandler(msg: Message, dialog_manager: DialogManager, bot: Bot):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    user_id = msg.from_user.id
    query = select(User).filter_by(id=user_id)
    user = await session.scalar(query)
    if user:
        await dialog_manager.start(
            state=StartStates[user.role], mode=StartMode.RESET_STACK
        )
    else:
        query = select(User).filter_by(role=Roles.ADMIN)
        admins = await session.scalars(query)
        builder = InlineKeyboardBuilder()
        builder.button(
            text="добавить в базу",
            callback_data=UserActionCb(action=UserActions.ADD, user_id=user_id),
        )
        builder.button(
            text="удалить сообщение",
            callback_data=UserActionCb(action=UserActions.PASS),
        )
        builder.adjust(1)
        for admin in admins:
            await bot.send_message(
                admin.id,
                "кто-то запустил бота!",
                reply_markup=builder.as_markup(),
            )


@router.callback_query(UserActionCb.filter(F.action == UserActions.ADD))
async def add_user_to_db(
    callback: CallbackQuery,
    callback_data: dict,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(
        AddUserSG.role_choice,
        data=callback_data["user_id"],
        mode=StartMode.RESET_STACK,
    )
    await callback.answer()


@router.callback_query(UserActionCb.filter(F.action == UserActions.PASS))
async def pass_and_del_msg(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
