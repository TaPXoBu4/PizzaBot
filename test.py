from sqlalchemy import Select, create_engine
from sqlalchemy.orm import Session
from config import Roles, StartStates, settings
from db.models import User


# engine = create_engine(settings.sqlite_sync_dsn, echo=True)

# with Session(engine) as session:
#     session.query(User).filter_by(role=Roles.ADMIN).delete()
#     session.commit()

# with Session(engine) as session:
#     query = Select(User).filter_by(role=Roles.ADMIN)
#     users = session.scalars(query).all()
#     print(users)
print(Roles.ADMIN)
