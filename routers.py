from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Const
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from config import StartStates
from db.models import User

start_router = Router()


class VerifySG(StatesGroup):
    main = State()


@start_router.message(CommandStart())
async def start_nandler(msg: Message, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    query = select(User).filter_by(id=msg.from_user.id)
    user = await session.scalar(query)
    if user:
        await dialog_manager.start(
            state=StartStates[user.role], mode=StartMode.RESET_STACK
        )
    else:
        await dialog_manager.start(state=VerifySG.main)


verify_dialog = Dialog(
    Window(
        Const('Введите пароль')
        state=VerifySG.main,
    )
)
