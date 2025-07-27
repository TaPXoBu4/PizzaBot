from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()
    shift_calc = State()
