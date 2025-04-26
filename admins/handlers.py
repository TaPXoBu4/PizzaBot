from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.input import ManagedTextInput
from sqlalchemy.ext.asyncio import AsyncSession

from admins.states import AddUserSG
from db.models import User


async def next_or_end(dm: DialogManager):
    if dm.dialog_data.get("finished"):
        await dm.switch_to(state=AddUserSG.preview)
    else:
        await dm.next()


async def on_role(
    event: CallbackQuery,
    select: Widget,
    dialog_manager: DialogManager,
    role: str,
    /,
):
    dialog_manager.dialog_data["role"] = role
    await next_or_end(dialog_manager)


async def on_enter_name(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    data: str,
    /,
):
    dialog_manager.dialog_data["username"] = message.text
    await next_or_end(dialog_manager)


async def on_confirm_user(clb: CallbackQuery, button, manager: DialogManager):
    session: AsyncSession = manager.middleware_data["session"]
    session.add(
        User(
            id=manager.start_data,
            name=manager.dialog_data["username"],
            role=manager.dialog_data["role"],
        )
    )
    await session.commit()
    await manager.done()
