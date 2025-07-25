from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from orders.states import OrderSG


async def next_or_end(dialog_manager: DialogManager):
    if dialog_manager.dialog_data.get("finished"):
        await dialog_manager.switch_to(OrderSG.preview)
    else:
        await dialog_manager.next()


async def on_area(event, select, dialog_manager: DialogManager, data: str):
    dialog_manager.dialog_data["area"] = int(data)
    await next_or_end(dialog_manager)


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
