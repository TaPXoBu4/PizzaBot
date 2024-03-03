from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

import getters
from states import CourierMainSG, CourierNewOrderSG

main_dialog = Dialog(
    Window(
        Const('Главное меню:'),
        Start(Const('Новый заказ'), id='new_c_order', state=CourierNewOrderSG.location),
        SwitchTo(Const('Заказы'), id='c_orders', state=CourierMainSG.orders),
        SwitchTo(Const('Смена'), id='c_shift', state=CourierMainSG.shift),
        SwitchTo(Const('За месяц'), id='c_month', state=CourierMainSG.month),
        state=CourierMainSG.main
    ),
    Window(
        Format('Заказы за {shift_date}'),
        getter=getters.orders_getter,
        state=CourierMainSG.orders
    )
)

new_order_dialog = Dialog(
    Window(
        Const('Выберите локацию:'),
        # Radio(),
        state=CourierNewOrderSG.location
    )
)
