from aiogram_dialog import DialogManager


async def add_user_result_getter(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["finished"] = True
    return dialog_manager.dialog_data
