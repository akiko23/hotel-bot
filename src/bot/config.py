from dataclasses import dataclass

import tomli


@dataclass
class DbConfig:
    user: str = "postgres"
    password: str = "postgres"
    name: str = "postgres"
    host: str = "localhost"
    port: int = 5432

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379

    @property
    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


@dataclass
class BotConfig:
    token: str
    admin_secret_key: str


@dataclass
class Config:
    bot: BotConfig
    db: DbConfig
    redis: RedisConfig


def load_config(path: str) -> Config:
    with open(path, mode="rb") as fp:
        data = tomli.load(fp)
    return Config(
        bot=BotConfig(**data["bot"]),
        db=DbConfig(**data["db"]),
        redis=RedisConfig(**data["redis"]),
    )
