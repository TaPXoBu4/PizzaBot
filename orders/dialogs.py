from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Column, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from orders.getters import areas_getter, orders_getter, payments_getter, preview_getter
from orders.handlers import (
    address_handler,
    confirm_order,
    int_factory,
    on_area,
    on_order,
    on_payment,
    price_handler,
    wrong_price,
)
from orders.states import OrderSG, OrdersSG

orders = Dialog(
    Window(
        Const("Заказы за сегодня:"),
        Column(
            Select(
                Format("{item.address}, {item.price}₽, {item.payment}"),
                id="s_orders",
                item_id_getter=lambda x: x.id,
                items="orders",
                on_click=on_order,
            )
        ),
        Cancel(Const("Назад")),
        SwitchTo(Const("Архив"), id="to_archive", state=OrdersSG.calendar),
        state=OrdersSG.main,
        getter=orders_getter,
    ),
    Window(
        Const("Выбери дату:"),
        state=OrdersSG.calendar,
    ),
)


order = Dialog(
    Window(
        Const("Выбери локацию:"),
        Column(
            Select(
                Format("{item.name}"),
                id="s_areas",
                item_id_getter=lambda item: item.id,
                items="areas",
                on_click=on_area,
            )
        ),
        Cancel(Const("Отмена")),
        state=OrderSG.location,
        getter=areas_getter,
    ),
    Window(
        Const("Введи адрес заказа:"),
        TextInput(
            id="address_input",
            on_success=address_handler,
        ),
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
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
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
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
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
        state=OrderSG.payment,
        getter=payments_getter,
    ),
    Window(
        Const("Твой заказ:"),
        Format("<i>локация</i>: {area_name}"),
        Format("<i>адрес</i>: {address}"),
        Format("<i>цена</i>: {price}"),
        Format("<i>тип оплаты</i>: {payment}"),
        Cancel(Const("Подтвердить"), on_click=confirm_order),
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
        state=OrderSG.preview,
        getter=preview_getter,
    ),
)
