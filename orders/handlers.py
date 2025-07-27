from datetime import datetime
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from config import Roles
from db.models import Order, User
from orders.states import OrderSG


async def next_or_end(dialog_manager: DialogManager):
    if dialog_manager.dialog_data.get("finished"):
        await dialog_manager.switch_to(OrderSG.preview)
    else:
        await dialog_manager.next()


async def on_area(event, select, dialog_manager: DialogManager, data: str):
    dialog_manager.dialog_data["area_id"] = int(data)
    await next_or_end(dialog_manager)


async def on_order(event, select, dialog_manager: DialogManager, data: str):
    pass


async def address_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    data: str,
):
    dialog_manager.dialog_data["address"] = data
    await next_or_end(dialog_manager)


def int_factory(data: str) -> int:
    if not data.isdigit():
        raise ValueError
    return int(data)


async def price_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    data: int,
):
    dialog_manager.dialog_data["price"] = data
    await next_or_end(dialog_manager)


async def wrong_price(message: Message, *args):
    await message.answer("Это херня какая-то, а не цена! Давай по-новой!")


async def on_payment(event, select, dialog_manager: DialogManager, data: str):
    dialog_manager.dialog_data["payment"] = data
    await next_or_end(dialog_manager)


async def confirm_order(clb: CallbackQuery, button, manager: DialogManager):
    session: AsyncSession = manager.middleware_data["session"]
    user = await session.get(User, clb.from_user.id)
    manager.dialog_data.update(
        courier_id=clb.from_user.id if user.role == Roles.COURIER else None,
        dttm=datetime.now().replace(microsecond=0, second=0),
    )
    del manager.dialog_data["area_name"]
    order = Order(**manager.dialog_data)
    session.add(order)
    await session.commit()

    await clb.answer("Заказ создан", show_alert=True)
