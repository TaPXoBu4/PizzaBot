from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from config import Payments
from orders.getters import areas_getter, payments_getter
from orders.handlers import (
    address_handler,
    int_factory,
    on_area,
    on_payment,
    price_handler,
    wrong_price,
)
from orders.states import OrderSG, OrdersSG

orders = Dialog(
    Window(
        Select(
            Format("item[address], item[price]₽, item[payment]"),
            id="s_orders",
            item_id_getter=lambda x: x["id"],
            items="orders",
        ),
        Cancel(Const("Назад")),
        SwitchTo(Const("Архив"), id="to_archive", state=OrdersSG.calendar),
        state=OrdersSG.main,
    ),
    Window(
        state=OrdersSG.calendar,
    ),
)


order = Dialog(
    Window(
        Const("Выбери локацию:"),
        Select(
            Format("{item.name}"),
            id="s_areas",
            item_id_getter=lambda item: item.id,
            items="areas",
            on_click=on_area,
        ),
        state=OrderSG.location,
        getter=areas_getter,
    ),
    Window(
        Const("Введи адрес заказа:"),
        TextInput(
            id="address_input",
            on_success=address_handler,
        ),
        state=OrderSG.address,
    ),
    Window(
        Const("Укажи цену:"),
        TextInput(
            id="price_input",
            type_factory=int_factory,
            on_success=price_handler,
            on_error=wrong_price,
        ),
        state=OrderSG.price,
    ),
    Window(
        Const("Выбери тип оплаты:"),
        Select(
            Format("{item.value}"),
            id="s_payments",
            item_id_getter=lambda item: item.value,
            items="payments",
            on_click=on_payment,
        ),
        state=OrderSG.payment,
        getter=payments_getter,
    ),
    Window(
        Const("Твой заказ:"),
        Format("<i>локация</i>: {area}"),
        Format("<i>адрес</i>: {address}"),
        Format("<i>цена</i>: {price}"),
        Format("<i>тип оплаты</i>: {payment}"),
        state=OrderSG.preview,
    ),
)
