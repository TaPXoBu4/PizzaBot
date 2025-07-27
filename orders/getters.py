from datetime import date
from aiogram_dialog import DialogManager
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Payments, Roles
from db.models import Area, Order, User


async def areas_getter(dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    areas = await session.scalars(select(Area))
    return {"areas": areas}


async def payments_getter(**kwargs):
    return {"payments": list(Payments)}


async def preview_getter(dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    area: Area = await session.get(Area, dialog_manager.dialog_data["area_id"])
    dialog_manager.dialog_data["area_name"] = area.name
    return dialog_manager.dialog_data


async def orders_getter(dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    userid = dialog_manager.event.from_user.id
    dttm = date.today()
    user = await session.get(User, userid)
    criteria = [func.date(Order.dttm) == dttm]

    if user.role == Roles.COURIER:
        criteria.append(Order.courier_id == userid)

    stmt = select(Order).filter(*criteria)
    orders = await session.scalars(stmt)
    return {"orders": orders.all()}
