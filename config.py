from enum import StrEnum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from admins.states import MainSG as admin_mainsg
from couriers.states import MainSG as courier_mainsg


class Roles(StrEnum):
    ADMIN = "админ"
    COURIER = "курьер"


class Payments(StrEnum):
    CASH = "наличные"
    TERMINAL = "терминал"
    PAID = "оплачено"


StartStates = {
    Roles.ADMIN.value: admin_mainsg.main,
    Roles.COURIER.value: courier_mainsg.main,
}


class Settings(BaseSettings):
    bot_token: SecretStr
    db_name: str
    passwd: SecretStr

    @property
    def sqlite_async_dsn(self):
        return f"sqlite+aiosqlite:///{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
