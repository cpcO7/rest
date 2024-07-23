import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv('../.env')

TOKEN = os.getenv("BOT_TOKEN")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config import conf
from tlg_bot.bot.handlers import private_handler_router


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{conf.bot.BASE_WEBHOOK_URL}{conf.bot.WEBHOOK_PATH}", secret_token=conf.bot.WEBHOOK_SECRET)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


async def main_pooling() -> None:
    dp = Dispatcher()
    dp.include_router(private_handler_router)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


def main_webhook() -> None:
    dp = Dispatcher()
    dp.include_router(private_handler_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=conf.bot.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=conf.bot.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=conf.bot.WEB_SERVER_HOST, port=conf.bot.WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main_webhook()
    # asyncio.run(main_pooling())
