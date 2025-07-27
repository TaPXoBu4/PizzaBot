from enum import StrEnum

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from admins.states import AddUserSG, MainSG as AdmMainSG
from couriers.states import MainSG as CouMainSG
from config import Roles
from db.models import User

router = Router()


class UserActions(StrEnum):
    ADD = "add"
    BAN = "ban"
    PASS = "pass"


class UserActionCb(CallbackData, prefix="user_action"):
    action: str
    user_id: int | None = None


def start_kb(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="добавить в базу",
            callback_data=UserActionCb(action=UserActions.ADD, user_id=user_id).pack(),
        ),
        InlineKeyboardButton(
            text="удалить сообщение",
            callback_data=UserActionCb(action=UserActions.PASS).pack(),
        ),
    )
    builder.adjust(2)
    return builder.as_markup()


@router.message(CommandStart())
async def start_handler(msg: Message, dialog_manager: DialogManager, bot: Bot):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    user_id = msg.from_user.id
    user = await session.get(User, user_id)
    if user:
        start_state = AdmMainSG.main if user.role == Roles.ADMIN else CouMainSG.main
        await dialog_manager.start(state=start_state, mode=StartMode.RESET_STACK)
    else:
        stmt = select(User).filter_by(role=Roles.ADMIN)
        admins = await session.scalars(stmt)
        admins = admins.all()

        for admin in admins:
            await bot.send_message(
                admin.id,
                "кто-то запустил бота!",
                reply_markup=start_kb(user_id),
            )
        # await msg.answer(f"Ваш ID = {msg.from_user.id}")


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
