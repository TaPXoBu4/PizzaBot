from db.schema import DB_NAME, CREATE_SCRIPT
from db.models import DataBase, SqLiteDataBase

database = SqLiteDataBase(DB_NAME, CREATE_SCRIPT)


class UserService:
    db: DataBase = database

    @classmethod
    def get_user(cls, userid):
        query = 'SELECT * FROM users WHERE id = ?'
        return cls.db.select_query(query, [userid])

    @classmethod
    def get_users_by_status(cls, status):
        query = 'SELECT * FROM users WHERE status = ?'
        return cls.db.select_query(query, [status])

    @classmethod
    def add_user(cls, userid, username, status):
        query = 'INSERT INTO users(id, name, status) VALUES (?, ?, ?)'
        cls.db.post_query(query, [userid, username, status])


class OrderService:
    db: DataBase = database

    @classmethod
    def get_orders(cls, date, userid=None):
        if userid:
            query = 'SELECT * FROM orders WHERE '