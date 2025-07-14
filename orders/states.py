from aiogram.fsm.state import State, StatesGroup


class OrderSG(StatesGroup):
    location = State()
    address = State()
    price = State()
    payment = State()
    preview = State()
