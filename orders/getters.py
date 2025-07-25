from aiogram_dialog import DialogManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Payments
from db.models import Area


async def areas_getter(dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    areas = await session.scalars(select(Area))
    return {"areas": areas}


async def payments_getter(diaog_manager: DialogManager, **kwargs):
    return {"payments": list(Payments)}
