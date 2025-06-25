from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja

from admins.getters import add_user_result_getter
from admins.handlers import on_confirm_user, on_enter_name, on_role
from admins.states import AddUserSG, MainSG
from config import Roles

CANCEL_EDIT = SwitchTo(
    Const("Отменить редактирование"),
    when=F["dialog_data"]["finished"],
    id="cnl_edt",
    state=AddUserSG.preview,
)

main_dialog = Dialog(
    Window(
        Button(Const("Новый заказ"), id="to_new_order"),
        Button(Const("Заказы за смену"), "to_shift_orders"),
        Button(Const("Рассчитать курьеров"), id="to_courier_calculation"),
        Button(Const("Админка"), id="to_adminka"),
        state=MainSG.main,
    ),
)

add_user = Dialog(
    Window(
        Const("Роль нового сотрудника:"),
        Select(
            Format("{item}"),
            id="select_role",
            items=[Roles.ADMIN, Roles.COURIER],
            item_id_getter=lambda x: x,
            on_click=on_role,
        ),
        CANCEL_EDIT,
        Cancel(Const("Отмена")),
        state=AddUserSG.role_choice,
    ),
    Window(
        Const("Введите имя нового сотрудника:"),
        TextInput(id="enter_name", on_success=on_enter_name),
        CANCEL_EDIT,
        Cancel(Const("Отмена")),
        state=AddUserSG.enter_name,
    ),
    Window(
        Jinja(
            "<u>Новый сотрудник:</u>\n\n<b>Имя</b>: {{username}}\n<b>Роль</b>: {{role}}"
        ),
        SwitchTo(
            Const("Изменить роль"),
            id="to_select_role",
            state=AddUserSG.role_choice,
        ),
        SwitchTo(
            Const("Изменить имя"),
            id="to_enter_name",
            state=AddUserSG.enter_name,
        ),
        Button(Const("Подвердить"), id="confirm_user", on_click=on_confirm_user),
        Cancel(Const("Отмена")),
        state=AddUserSG.preview,
        getter=add_user_result_getter,
    ),
)

