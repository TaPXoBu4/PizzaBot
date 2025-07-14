from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db.models import Base, User, Order, Location
from pizzabot import engine

# Инициализируем FastAPI и SQLAdmin
app = FastAPI()
admin = Admin(app, engine)


# View для моделей
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.role]
    column_searchable_list = [User.name, User.role]
    column_filters = [User.role]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.dttm, Order.price, Order.payment, Order.courier]
    column_searchable_list = [Order.payment]
    column_filters = [Order.payment, Order.dttm, Order.price]
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-box"


class LocationAdmin(ModelView, model=Location):
    column_list = [Location.id, Location.name, Location.price]
    column_searchable_list = [Location.name]
    column_filters = [Location.price]
    name = "Локация"
    name_plural = "Локации"
    icon = "fa-solid fa-map-pin"


# Регистрируем
admin.add_view(UserAdmin)
admin.add_view(OrderAdmin)
admin.add_view(LocationAdmin)
