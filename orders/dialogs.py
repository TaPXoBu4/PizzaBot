from aiogram_dialog import Dialog, Window

from orders.states import NewOrderSG


new_order = Dialog(
    Window(state=NewOrderSG.location),
    Window(state=NewOrderSG.address),
    Window(state=NewOrderSG.price),
    Window(state=NewOrderSG.payment),
    Window(state=NewOrderSG.preview),
)
