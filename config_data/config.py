from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    PAYMENTS_TOKEN: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    """Read the .env file and return an instance of the Config
        class

    Args:
        path: path to the .env file

    Returns: instance of the Config class

    """
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        BOT_TOKEN=env('BOT_TOKEN'),
        ADMIN_IDS=list(map(int, env.list('ADMIN_IDS'))),
        PAYMENTS_TOKEN=env('PAYMENTS_TOKEN')
    )
    )
