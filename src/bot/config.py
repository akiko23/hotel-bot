from dataclasses import dataclass
from typing import Optional

import tomli


@dataclass
class DbConfig:
    user: str = "postgres"
    password: str = "postgres"
    name: str = "postgres"
    host: str = "localhost"
    port: int = 5432

    @property
    def dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class BotConfig:
    token: str
    admin_secret_key: str
    

@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config(path: str):
    with open(path, mode="rb") as fp:
        data = tomli.load(fp)
    return Config(
        bot=BotConfig(**data["bot"]),
        db=DbConfig(**data["db"]),
    )

