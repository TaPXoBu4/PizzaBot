from datetime import date
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from config import Roles, settings
from db.models import Order, User


engine = create_engine(settings.sqlite_sync_dsn, echo=False)

# with Session(engine) as session:
#     session.query(User).filter_by(role=Roles.ADMIN).delete()
#     session.commit()

# with Session(engine) as session:
#     query = Select(User).filter_by(role=Roles.ADMIN)
#     users = session.scalars(query).all()
#     print(users)

with Session(engine) as session:
    # session.add(User(id=5963726977, name="Марат", role=Roles.COURIER))
    # session.commit()
    user: User = session.scalar(select(User).filter(User.role == Roles.COURIER))
    orders = user.orders.filter(func.date(Order.dttm) == date.today()).all()

[print(o.as_dict()) for o in orders]
