from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
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
    Window(state=OrderSG.location),
    Window(state=OrderSG.address),
    Window(state=OrderSG.price),
    Window(state=OrderSG.payment),
    Window(state=OrderSG.preview),
)
