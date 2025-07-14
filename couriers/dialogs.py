from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Button
from aiogram_dialog.widgets.text import Const

from couriers.states import MainSG
from orders.states import NewOrderSG

main_dialog = Dialog(
    Window(
        Start(Const("Новый заказ"), state=NewOrderSG),
        Button(Const('Заказы')),
        state=MainSG.main,
    ),
)
