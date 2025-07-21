from aiogram.fsm.state import State, StatesGroup


class OrdersSG(StatesGroup):
    main = State()
    calendar = State()


class OrderSG(StatesGroup):
    location = State()
    address = State()
    price = State()
    payment = State()
    preview = State()
