import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BaseConfig:
    def asdict(self):
        return asdict(self)


@dataclass
class DatabaseConfig(BaseConfig):
    """Database connection variables"""
    NAME: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USER')
    PASS: str = os.getenv('DB_PASS')
    HOST: str = os.getenv('DB_HOST')
    PORT: str = os.getenv('DB_PORT')

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


@dataclass
class BotConfig(BaseConfig):
    """Bot configuration"""
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')

    WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
    WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))

    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")

    # MAIN_BOT_PATH: str = "/webhook/main"
    # OTHER_BOTS_PATH: str = "/webhook/bot/{bot_token}"
    #
    # OTHER_BOTS_URL: str = f"{BASE_URL}{OTHER_BOTS_PATH}"

    @property
    def get_admin_list(self):
        return list(map(int, self.ADMIN_LIST.split(',')))


@dataclass
class RedisConfig(BaseConfig):
    """Redis configuration"""
    URL: str = os.getenv('REDIS_URL')
    DB: str = os.getenv('REDIS_DB')
    HOST: str = os.getenv('REDIS_HOST')
    PORT: str = os.getenv('REDIS_PORT')


@dataclass
class WebConfig(BaseConfig):
    """Web configuration"""
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    USERNAME: str = os.getenv('ADMIN_USERNAME')
    PASSWD: str = os.getenv('ADMIN_PASSWORD')


@dataclass
class Configuration:
    """All in one configuration's class"""
    rd = RedisConfig()
    db = DatabaseConfig()
    bot = BotConfig()


conf = Configuration()
