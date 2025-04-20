from datetime import datetime
from typing import Annotated, List, Optional, Text

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from sqlalchemy.orm.properties import ForeignKey


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
    orders: Mapped[List["Order"]] = relationship(back_populates="courier")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, role={self.role!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[classic_id]
    dttm: Mapped[dttm]
    payment: Mapped[str]
    price: Mapped[Optional[int]]
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    courier: Mapped["User"] = relationship(back_populates="orders")
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locations.id"))
    info: Mapped[Optional[Text]]

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, dttm={self.dttm!r}, price={self.dttm!r}, payment={self.payment!r}, courier={self.courier.name!r})"


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[classic_id]
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, name={self.name!r})"
