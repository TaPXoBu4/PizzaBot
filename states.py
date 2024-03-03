from aiogram.fsm.state import StatesGroup, State


class AdminMainSG(StatesGroup):
    main = State()

class CourierMainSG(StatesGroup):
    main = State()
    orders = State()
    shift = State()
    month = State()

class CourierNewOrderSG(StatesGroup):
    location = State()
    address = State()
    price = State()
    paytype = State()