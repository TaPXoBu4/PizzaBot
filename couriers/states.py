from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()
    shift_calc = State()

class OrdersGS(StatesGroup):
    main = State()
    calendar = State()
