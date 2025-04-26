from aiogram.fsm.state import State, StatesGroup


class AddUserSG(StatesGroup):
    role_choice = State()
    enter_name = State()
    preview = State()


class MainSG(StatesGroup):
    main = State()
