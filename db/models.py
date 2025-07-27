from datetime import datetime
from typing import Annotated, List, Optional, Text

from config import Payments, Roles
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from sqlalchemy.sql.schema import ForeignKey

dttm = Annotated[datetime, mapped_column(default=datetime.now)]
baseid = Annotated[
    int,
    mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
]


class Base(DeclarativeBase):
    id: Mapped[baseid]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    """
    Модель пользователя (например, курьера или администратора).

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        name (str): Имя пользователя (уникальное).
        role (Roles): Роль пользователя в системе (например, COURIER, ADMIN).
        orders (List[Order]): Список заказов, закрепленных за этим пользователем.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Roles] = mapped_column(SQLEnum(Roles, name="user_role"))
    orders: Mapped[List["Order"]] = relationship(
        back_populates="courier", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, role={self.role!r})"


class Order(Base):
    """Модель заказа.
    Атрибуты:
        id (int): Уникальный идентификатор заказа.
        dttm (datetime): Дата и время создания заказа (по умолчанию — текущее).
        payment (Payments): Тип оплаты (enum).
        price (int | None): Стоимость заказа в рублях.
        courier_id (int | None): ID курьера, связанного с заказом.
        area_id (int | None): ID зоны доставки.
        address (str | None): Адрес доставки.
    """

    __tablename__ = "orders"

    dttm: Mapped[dttm]
    payment: Mapped[Payments] = mapped_column(SQLEnum(Payments, name="payment"))
    price: Mapped[Optional[int]]
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    courier: Mapped["User"] = relationship(back_populates="orders")
    area_id: Mapped[Optional[int]] = mapped_column(ForeignKey("areas.id"))
    address: Mapped[Optional[Text]]

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, dttm={self.dttm!r}, price={self.price!r}, payment={self.payment!r}, courier={self.courier_id!r})"


class Area(Base):
    __tablename__ = "areas"

    name: Mapped[str] = mapped_column(unique=True)
    tariff: Mapped[int]

    def __repr__(self) -> str:
        return f"Area(id={self.id!r}, name={self.name!r}, price={self.tariff!r})"
