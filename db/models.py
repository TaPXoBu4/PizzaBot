from datetime import datetime
from typing import Annotated, List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import StrEnum


class Roles(StrEnum):
    ADMIN = "admin"
    COURIER = "courier"


class Base(DeclarativeBase):
    pass


dttm = Annotated[datetime, mapped_column(default=datetime.now)]
classic_id = Annotated[
    int,
    mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
]


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str]
    orders: Mapped[List['Order']] = relationship(back_populates='courier')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, role={self.role!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[classic_id]
    location: 

    def __repr__(self) -> str:
        return f"Condition(id={self.condition_id!r}, zone={self.zone!r}, dttm={self.dttm!r}, condition={self.condition!r})"


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[classic_id]
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, name={self.name!r})"
