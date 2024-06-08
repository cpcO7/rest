from aiogram import Router

from tlg_bot.bot.handlers.private.main_handler import main_router

private_handler_router = Router()

private_handler_router.include_routers(
    main_router
)
