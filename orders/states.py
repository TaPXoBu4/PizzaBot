from aiogram.fsm.state import State, StatesGroup


class NewOrderSG(StatesGroup):
    location = State()
    address = State()
    price = State()
    payment = State()
    preview = State()
