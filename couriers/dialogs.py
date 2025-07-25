from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const
from couriers.states import MainSG, OrdersGS
from orders.states import OrderSG

main_dialog = Dialog(
    Window(
        Start(Const("Новый заказ"), id="to_new_order", state=OrderSG.location),
        Start(Const("Заказы"), id="to_orders", state=OrdersGS.main),
        SwitchTo(
            Const("Рассчитать смену"),
            id="to_shift_calc",
            state=MainSG.shift_calc,
        ),
        state=MainSG.main,
    ),
)
